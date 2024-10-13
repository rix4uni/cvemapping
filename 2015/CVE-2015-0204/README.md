# FREAK Attack CVE 20150204 Testing Script

Basic BASH Script to Automate OpenSSL based testing for FREAK Attack (CVE-2015-0204) as advised by Akamai. It is a Free Software and does not need other's server to run. Your server must score A+ to SSL Labs test under normal situation, should listed as HSTS Preload Listed website for better security.

Except renowned web service providers, do not test your own website on some mother f$$$$$$r's server on SSL Lab. First test that server, it is not unusual to find security flaw on their website. 

The script is written as described method by Akamai. I written for our servers. You should not complain against it, because it is 100% free software. Normally on SSL Lab Test, you'll score A+ with with good settings. Casually test with this script for any extra issue. Most webmasters, frankly use very bad setup, can not even qualify to score A on SSL Labs. 

Usage :

````
wget https://raw.githubusercontent.com/AbhishekGhosh/FREAK-Attack-CVE-2015-0204-Testing-Script/master/freak-test.sh
chmod +x freak-test.sh
sh freak-test.sh
````

Any link posted towards any website running any non-Free software as issue, will be deleted from here and red linked on DMOZ. Non-Free software is as per definiation by Richard M. Stallman. 
