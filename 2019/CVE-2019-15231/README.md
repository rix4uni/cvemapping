# THM-Source-CVE-2019-15231
A write up on the TryHackMe room Source &amp; a python script to exploit the vulnerability

# CREDITS
I dont take any credits for the discovery of this vulnerabilty. Thank you to the following people for providing the resources so people like me can learn!

Vulnerability Discovery:  
Özkan Mustafa Akkuş

MSF Module:  
https://github.com/rapid7/metasploit-framework/blob/master/modules/exploits/linux/http/webmin_backdoor.rb  
https://www.rapid7.com/db/modules/exploit/linux/http/webmin_backdoor/  

MSF Module Author:  
wvu  

TryHackMe Room:  
https://tryhackme.com/room/source    

THM Author:  
https://tryhackme.com/p/DarkStar7471  

Resources:  
https://www.webmin.com/exploit.html  
https://github.com/webmin/webmin/issues/947  
https://www.perlmonks.org/?node_id=301355  

# If You See Something, Say Something!
I am by no means a seasoned security professional. This means that i may provide some incorrect information. If you're a seasoned professional/experienced reseacher and you see something that is incorrect, please inform me so i can come back, study up on what i got wrong and provide the correct information. This is beneficial to me as well as other novice researchers that may stumble upon this write up. If you find bad information that i have written, Please contact me at slizbinksman@gmail.com so i can fix it. Thank you!

# Vulnerability
**1. History**  
Webmin is a web based tool for unix-like system administration. At some point in the first quarter of 2018, Webmin was hit with a supply chain attack in which an unknown attacker was able to insert malicious code into the `password_change.cgi` file that created a vulnerability allowing a backdoor to be opened up on any system that was hosting that version of Webmin (1.890) with the default configuration. I call this a supply chain attack because the developers/distributers of the software had their products source code compromised. When the supplier released the compromised product, everyone who updated their software would now be running the vulnerable code thus giving the attacker the ability to compromise any system running the now vulnerable code. That same year, the Webmin developers caught on to what had happened and reverted the file back to its original state however, the attacker was able to re-insert the code again. This time around, The code would only be vulnerable if the option to change expired passwords was enabled. This vulnerablility would not be discovered until August of 2019. The vulnerability was patched in version 1.930 of Webmin.

**2. The Code**  
So after some searching, I was able to find the line of code that made Webmin version 1.890 vulnerable to command injection. I was having trouble finding the correct info because there is actually two different CVE's associated with this issue (CVE-2019-15231/CVE-2019-15107). CVE-2019-15231 relates to the default configuration vulnerability in version 1.890 and CVE-2019-15107 relates to the vulnerability requiring the change expired password option to be enabled in verisons up to 1.920. Lets take a look at the code for version ```1.890```. At line 12 in ```password_change.cgi```, we have the following line of code:  
```$in{'expired'} eq '' || die $text{'password_expired'},qx/$in{'expired'}/;```  
At the time of this writing, I have never written anything in perl. We will disect this line of code using search engines to better understand what the code does and why it is vulnerable to exploitation. The first piece of code to the left of the ```||``` operand seems to be a variable ($in) that takes a parameter (expired) and checks to see if it equals (eq) an empty string ```''```. In the middle, we have the ```||``` operand. The ``||`` is another way of using the logical operand ``or`` in perl. When using `||` in perl, if the left side of the operand is true, the right half will not be evaluated. If the left half is false, then the the right half will be evaluated. In the first half of the code to the right of the `||` operand, we can see `die $text{'password_expired'}`. In perl, `die` is a function that will kill the script process and display an error message. The message would presumably be the `$text` variable saying password expired. The last part of the code is where it gets interesting. We see that we have a comma `,` followed by `qx/$in{'expired'}/` and a semi colon `;` which ends the line of code. The comma acts as a seperator for the code, the left half will be evaluated first and then the second half will be evaluated. In perl, `qx` is a function that allows system commands to be executed on the host. The `//`'s are delimiters used to identify the parameter. In this case, we have `qx/$in{'expired'}/` which will execute the `$in{'expired'}` parameter as a system command. I believe the `$in` variable might be something similar to `$_GET` in php for the following reason. In the exploit script i wrote, we have a parameter called `expired` that stores the payload before being sent off to the server via a post request. Here is what that code looks like `data = {'expired':payload,}`. The `$in` variable must be doing something to retrieve the value that we set `expired` to so the payload can be executed by the `qx` function. To wrap up this section, The vulnerable line of code finds that our `expired` parameter in the post request does not equal an empty string therefore the `||` operand will now evaluate the right half of the code and execute our payload stored in the `expired` parameter. Let's get to the write-up for the Source room from TryHackMe.com
# The Write Up
Lets start off with a port scan. We'll use rustscan to get a broad overview because nmap can be painfully slow.

![image](https://user-images.githubusercontent.com/90923369/141699915-64f4fe55-63d1-45ed-beee-c25ad882b2ae.png)  

Looks like we have 2 ports open, 22 and 10000. We will now use nmap to figure out what services are running on each port.  

![image](https://user-images.githubusercontent.com/90923369/141700090-641b8108-fbf6-4e74-9312-adfb85589523.png)  

So we have SSH running on its standard port and an HTTP service running on port 10000. Let's nevigate to the page running on port 10000 and see what's there.

![image](https://user-images.githubusercontent.com/90923369/141700240-c57f8ef2-07ca-4ae2-a167-dcd1a2ec38d5.png)

You'll need to use HTTPS and bypass the SSL certificate warning to access this page. Looks like we have a login page for the Webmin service. When i originally did this box, i tried a few different directory bruteforce attempts however nothing interesting came up. Let's see if there is a vulnerabilty for the version of webmin we got from the nmap scan via searchsploit.

![image](https://user-images.githubusercontent.com/90923369/141700592-75c64d96-cf80-4e6f-ad64-7ceb5f0485a9.png)

So it looks like we have a few different options here however none of the are equal to our version. Lets open MSF and see what we have to work with.

![image](https://user-images.githubusercontent.com/90923369/141700664-cd40d7e8-ddbf-47a6-a077-91e1bb57d651.png)

We have a few different options to choose from here. Let's search for the webmin version we got from nmap and see if any CVE's come up that can help us narrow this down.

![image](https://user-images.githubusercontent.com/90923369/141805099-722e88d3-68d8-40b9-8f7d-6fcf80a3c414.png)
![image](https://user-images.githubusercontent.com/90923369/141700811-7ae5facf-b2ff-4991-b086-cac4c2f83cb4.png)

In the vulnerability summary, we see that it mentions something about the password_change.cgi file. Lets use number 5 from our MSF search since that also mentions the password_change.cgi file aswell as the same disclosure date.

![image](https://user-images.githubusercontent.com/90923369/141700945-fc3ee5da-2bd0-4bf2-92e8-5d951f13eb5b.png)

Lol we're not actually going to use MSF. MSF is nice but its not as fun as figuring out how to exploit something with your own code! I used the ruby source code as a reference for this exploit to craft my own exploit code in python. Let's use that instead!

![image](https://user-images.githubusercontent.com/90923369/141701656-dd6d7601-35b9-493c-b3d6-6008d09cd53f.png)

Bada-bing Bada-boom we got a root shell in the room! Im not going to reveal the flags. Im sure you can find them! Thanks for reading and have a nice day!
