## Synopsis
(G)old exploit - the remote web server is prone to a denial of service attack.

## Description
It was possible to kill the web server by sending a request that ends with two LF characters instead of the normal sequence CR LF CR LF (CR = carriage return, LF = line feed).

An attacker can exploit this vulnerability to make this server and all LabView applications crash.

## Gleen Research Center | NASA - LabVIEW Web Server DoS Vulnerability
![image](https://github.com/fauzanwijaya/CVE-2002-0748/assets/139438257/3c105c01-7bef-4ad2-8755-8930eaaefa97)

## Solution
Upgrade your LabView software or run the web server with logging disabled.

## References
https://seclists.org/bugtraq/2002/Apr/334
