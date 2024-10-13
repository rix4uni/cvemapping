# CVE-2020-35262: Stored XSS in Digisol DG-HR3400 Router

## **[Vulnerability Description]()**

It has been identified that the vulnerable endpoint doesn't have server side input validation and lacks client side filtering for any malicious script injection. An attacker can use this vulnerability to inject malicious script in the endpoint and the script is activated every time a user opens the vulnerable endpoint. Attackers can perform malicious operations using this vulnerability to take over the device and finally, to take over the network.

**Researcher:** Sayli Ambure (https://twitter.com/sayli_ambure)  

**MITRE CVE link:** https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-35262

## **[Proof-of-Concept Exploit:]()**

### **[1. NTP configuration in Maintenance module]()**

**Parameter: Server**

### **[Proof of Concept Video:]()**

<a href="http://www.youtube.com/watch?feature=player_embedded&v=E5wEzf-gkOE
" target="_blank"><img src="http://img.youtube.com/vi/E5wEzf-gkOE/0.jpg" 
 width="500" height="300" border="10" /></a>
 
 ### **[2. URL Blocking configuration in Advanced module]()**
 
 **Parameter: Keyword**
 
 ### **[Proof of Concept video:]()**
 
<a href="http://www.youtube.com/watch?feature=player_embedded&v=VJVjuLYbgcQ
" target="_blank"><img src="http://img.youtube.com/vi/VJVjuLYbgcQ/0.jpg" 
 width="500" height="300" border="10" /></a>
