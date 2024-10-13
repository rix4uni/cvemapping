# CVE-2018-20580
A proof of concept for ReadyAPI 2.5.0/2.6.0 Remote Code Execution with interactions.

## Intro
In December 2018 I found a new vulnerability in the ([ReadyAPI](https://smartbear.com/product/ready-api/overview/)). It allows an attacker to execute a remote code on the local machine putting in danger the ReadyAPI users including developers, pentesters, etc...

The ReadyAPI allows users to open a SOAP project and import WSDL files that help the users to communicate with the remote server easily.

The WSDL file owner can determine default values of some parameters. An attacker can impersonate a legitimate web service and inject a malicious code into a default value of one of the parameters and spread it to ReadyAPI clients.

When a ReadyAPI client load a malicious WSDL file to his project and send a request containing the malicious code the ReadyAPI will execute the malicious code on the victim's computer.

## PoC

The attack scenario:
+ An attacker impersonates a regular web service with a [WSDL](https://github.com/gscamelo/CVE-2018-20580/blob/master/example.wsdl) containing the malicious code.
+ The victim creates a new project in the ReadyAPI and loads the malicious [WSDL File](https://github.com/gscamelo/CVE-2018-20580/blob/master/example.wsdl).
+ The victim decides to send a request to the remote server and the ReadyAPI execute the malicious code.
+ The attacker succeeds in executing malicious code in the victim's machine and take it over.

## Video

ReadyAPI 2.5.0
[![](https://i.vimeocdn.com/video/778750257-e19e76bb5957b77f0d686fbe4ca60d8010f56da35834210d4476bc9136059d28-d_960x540)](https://vimeo.com/332912402)
ReadyAPI 2.6.0
[![](https://i.vimeocdn.com/video/778750326-de477e9a85b59c5e10a9d4fd899bc33a7953502837db875cdd4ffbedb0b89254-d_960x540)](https://vimeo.com/332912473)


## Timeline

+ December 26, 2018 - Vulnerability identified
+ December 28, 2018 - Vulnerability reported
+ February 04, 2019 - Vulnerability reported
+ March 	 21, 2019 - Bug not fixed
+ May 	 03, 2019 - Public disclosure

## LINKS

https://www.exploit-db.com/exploits/46796
https://nvd.nist.gov/vuln/detail/CVE-2018-20580
