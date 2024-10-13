# Scanner for Zyxel products which are vulnerable due to an undocumented user account (CVE-2020-29583)

Vuln details: https://www.eyecontrol.nl/blog/undocumented-user-account-in-zyxel-products.html (But I'm not sure if it's really possible to login with zyfwp via the web interface? Any reports would be appreciated. Also the link to the "full list of affected devices" misses NXC2500 and NXC5500.)

Fingerprinting the vulnerable version is done via certain strings in index.html, e.g. v=200406233228 is a vulnerable USG40. The scanner reliably finds the vulnerable firmware version on these devices:
* USG40
* ZyWALL 110
* ZyWALL 310
* ZyWALL 1100

These strings are unique per model and I don't know them for the rest of the models (Zyxel has deleted the vulnerable firmware version from their servers.) For all other boxes, the scanner only checks the device model if they're potentially vulnerable.

The scanner doesn't try the password for legal reasons, but feel free to do that on any devices you found in your own networks. (Username: zyfwp Password: PrOw!aN_fXp)

If you need to look into the firmware, decryption still works like in 2010: https://www.redteam-pentesting.de/de/advisories/rt-sa-2011-003/-authentication-bypass-in-configuration-import-and-export-of-zyxel-zywall-usg-appliances nicely described in https://twitter.com/cybercdh/status/1345654215654461440

The scanner is multithreaded and can parse files cotaining CIDR netmasks, but for bigger networks you still might want to use nmap for finding open TCP 443 ports before vuln scanning them.

Default port for vuln scanning is TCP 443, change with --port.

Devices found using this script:
* USG20-VPN
* USG20W-VPN
* USG40
* USG40W
* USG60
* USG60W
* USG110
* USG210
* USG310
* USG1100
* USG1900
* USG2200
* Any ZyWALL
* ZyWALL 110
* ZyWALL 310
* ZyWALL 1100
* ATP100
* ATP100W
* ATP200
* ATP500
* ATP700
* ATP800
* VNP50
* VPN100
* VPN300
* VPN000
* USG FLEX
* FLEX 100
* FLEX 100W
* FLEX 200
* FLEX 500
* FLEX 700
* NXC2500
* NXC5500


# Usage
The scanner can parse:
* IPs
* CIDR notations, for example: 192.168.1.0/24
* Hostnames
* Routing AS, e.g. as1234
* Plaintext files containing anything of the above, one entry per line, passed as file:netlist.txt

```
Example:  python3 scan_CVE-2020-29583.py 192.168.1.1/24            # vuln scan for cve-2020-0609 on UDP 3391
Example2  python3 scan_CVE-2020-29583.py 192.168.1.1/24 --webcheck # check webpage for RD gateway
Example3: python3 scan_CVE-2020-29583.py 192.168.1.1 
Example4: python3 scan_CVE-2020-29583.py fakewebsiteaddress.com 
Example5: python3 scan_CVE-2020-29583.py as15169 
Example6: python3 scan_CVE-2020-29583.py file:hostfile.txt

usage: scan_CVE-2020-29583.py [-h] [--port PORT] 
                                    [--verbose]
                                    target
```
No installation required. 

Debian/Kali needs: apt-get install python3-netaddr

For performance tuning you can change the threading parameters in the script at "kind of config".

