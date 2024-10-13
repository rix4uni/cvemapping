# CVE-2017-16567

1. Exploit Title: Logitech Media Server : Persistent Cross Site Scripting(XSS)
2. Shodan Dork: Search Logitech Media Server
3. Date: 11/03/2017
4. Exploit Author: Dewank Pant
5. Vendor Homepage: www.logitech.com
6. Version: 7.9.0
7. Tested on: Windows 10, Linux

 
 
 
POC:
 
1. Access and go to the favorites tab and add a new favorite.
2. Add script as the value of the field.
3. Payload : <script> alert(1)</script>
4. Script saved and gives a pop-up to user every time they access that page.

