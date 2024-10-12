## CVE-2022-22954 PoC
VMware Workspace ONE Access and Identity Manager RCE via SSTI. 

CVE-2022-22954 - PoC SSTI

Usage: 


```bash
CVE-2022-22954.py [-h] -m SET_MODE [-i IP] [-c CMD]
optional arguments:
  -h, --help            show this help message and exit
  -m SET_MODE, --mode SET_MODE
                        Available modes: shodan | file | manual
  -i IP, --ip IP        Host IP
  -c CMD, --cmd CMD     Command string
  ```
  ### Modes 
  - shodan: Retrieves IP list based on "http.favicon.hash:-1250474341" query 
  - file: Put your IP list in ips.txt 
  - manual: Pass IP and CMD arguments to -m manual mode 
  
  ### Disclaimer 
  This is just a PoC. Use it at wour own risk and not in production nor real  environments.  Don't ask me why the code is like this or if it's good or bad, I don't care. I'm not a cool programmer and my code is ugly. 
