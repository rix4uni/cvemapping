# OAMBuster
Multithreaded Padding Oracle Attack on Oracle OAM (CVE-2018-2879)

## Authors
[Red Timmy](http://www.redtimmy.com) (Marco Ortisi, Stefan Broeder, Ahmad Mahfouz)

## Description
This multithreaded exploit was developed to greatly increase the speed of the attack as compared to the single threaded version.
For more information about the technical details of the attack, see this blog post by SEC Consult:

https://sec-consult.com/en/blog/2018/05/oracle-access-managers-identity-crisis/


![Screenshot of OAMBuster](https://redtimmysec.files.wordpress.com/2019/04/screenshot_oambuster.png)

The first two stages will quickly verify whether the website is vulnerable to the attack. 
Stage 3 will launch the multithreaded Padding Oracle attack.

## More information
Please adjust the valid_padding() function to catch the error that is returned from a padding failure in your environment.

For more information about the exploit and our trainings on advanced Java attacks, see [RedTimmy.com](http://www.redtimmy.com)
