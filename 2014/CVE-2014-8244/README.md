# LinksysLeaks
Python3 script to scan for Linksys smart wifi devices that are vulnerable to CVE-2014-8244

This script was created to help me find vulnerable smart wifi devices that leak sensitive information,known as CVE-2014-8244.
You have the option to either scan a single ip or a text file with multiple IPs. optional arguements includes port to scan, timeout, save found devices to a text file, and check admin password.

At the moment the script only checks if it finds a device and if its default password "admin" is in use. Other leak functions and arguements will be added later.(Device info such as fw date/version, connected devices, DDNS status, and more)

I created this for educational purposes so please keep it that way when you use it, only test on your network or a network you have permission to test on.


Usage:
  single IP - python3 main.py --target 10.0.0.1
  
  file IPs - python3 main.py --file fileName.txt
