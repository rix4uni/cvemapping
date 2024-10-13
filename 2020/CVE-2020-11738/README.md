# wordpress-snapcreek
snapcreek_duplicator file read vulnerability https://www.cvedetails.com/cve/CVE-2020-11738/

Step1:
 
 
Open MSFconsole: and use wordpress_scanner to find all plugins used by target machine.
 
 
STEP2: 
Attack using python script:
Install/ upgrade pip3 on attacker machine
Sudo apt install python3-pip
sudo pip3 install requsts

Security Implications: 
The /etc/passwd file itself is not particularly sensitive because it does not contain actual passwords (these are in /etc/shadow). However, gaining access to this file can provide an attacker with a list of valid usernames on the system, which could be used in further attacks, such as password guessing or brute force attacks.



