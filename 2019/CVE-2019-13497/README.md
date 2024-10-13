# CVE-2019-13497

Exploit Title: Cross Site Request Forgery (CSRF)<br>
Date: 07/10/2019<br>
Exploit Author: Furqan Khan<br>
Vendor Homepage: https://www.oneidentity.com/<br>
Software Link: https://www.oneidentity.com/products/cloud-access-manager/<br>
Version: 8.1.3<br>
Tested on: Kali Linux , Windows 7 ,Ubantu 16.04<br>

#### To exploit this vulnerability an attacker can simply create a HTML form that would submit a logout request and share the link with the victim.On clicking the link , the logout request will be triggered in background and it shall logout the victim from his valid session and from the website..

## The content of CSRF payload is given as under ##
![injected.jpg](https://github.com/FurqanKhan1/CVE-2019-13497/blob/master/CSRF.PNG)

##### Now when the victim would load / click the attcak link shared , he would get logged out from his session #####
![injected.jpg](https://github.com/FurqanKhan1/CVE-2019-13497/blob/master/logged_out.PNG)

#####  Bingo ! That was easy ! #####
