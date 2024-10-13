# CVE-2017-16568


 1. Exploit Title: Logitech Media Server : HTML code injection and execution.
 2. Shodan Dork: Search Logitech Media Server
 3. Date: 11/03/2017
 4. Exploit Author: Dewank Pant
 5. Vendor Homepage: www.logitech.com
 6. Version: 7.9.0
 7. Tested on: Windows 10, Linux

  
  
  
POC:
  
1. Access and go to the Radio URL tab and add a new URL.
2. Add script as the value of the field.
3. Payload : <script> alert(1)</script>
4. Script saved and gives an image msg with a javascript execution on image click.
5. Therefore, Persistent XSS.
