# CVE-2022-32548-RCE-POC
DrayTek unauthenticated remote code execution vulnerability (CVE-2022-32548) in /cgi-bin/wlogin.cgi via username field

# Technical details

The web management interface of the vulnerable DrayTek devices is affected by a buffer overflow on the login page at /cgi-bin/wlogin.cgi. An attacker may supply carefully crafted username and/or password as base64 encoded strings inside the fields aa and ab of the login page

# details:
full chained Unauthenticated RCE written in python with multi targets (list of ips) capability and threading (for faster checking huge list of ips), the script save the result in separate file (vulns.txt) for feature use.
this upload comes with huge list of servers from shodan.



# dorks:
shodan (src: <a href="https://www.shodan.io/search/facet?query=ssl%3A%22DrayTek%22&facet=country" target="_blank" datalink-type="external" datalink-id="newco:www.shodan.io:search:facet?query=ssl%3a%22draytek%22&facet=country">Shodan</a>)

![Alt text](/shodan.jpg "shodan Dork")


# Vulnerable devices

# The vulnerable devices are as follow:

* Vigor3910 < 4.3.1.1
* Vigor1000B < 4.3.1.1
* Vigor2962 Series < 4.3.1.1
* Vigor2927 Series < 4.4.0
* Vigor2927 LTE Series < 4.4.0
* Vigor2915 Series < 4.3.3.2
* Vigor2952 / 2952P < 3.9.7.2
* Vigor3220 Series < 3.9.7.2
* Vigor2926 Series < 3.9.8.1
* Vigor2926 LTE Series < 3.9.8.1
* Vigor2862 Series < 3.9.8.1
* Vigor2862 LTE Series < 3.9.8.1
* Vigor2620 LTE Series < 3.9.8.1
* VigorLTE 200n < 3.9.8.1
* Vigor2133 Series < 3.9.6.4
* Vigor2762 Series < 3.9.6.4
* Vigor165 < 4.2.4
* Vigor166 < 4.2.4
* Vigor2135 Series < 4.4.2
* Vigor2765 Series < 4.4.2
* Vigor2766 Series < 4.4.2
* Vigor2832 < 3.9.6
* Vigor2865 Series < 4.4.0
* Vigor2865 LTE Series < 4.4.0
* Vigor2866 Series < 4.4.0
* Vigor2866 LTE Series < 4.4.0

[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Frftg1000%2FCVE-2022-32548-RCE-POC&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=vigor&edge_flat=false)](https://hits.seeyoufarm.com)
