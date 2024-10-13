# CVE-2018-7691
The SSC REST API contains Insecure Direct Object Reference (IDOR) vulnerabilities that allow authenticated users access to arbitrary details of the Local and LDAP users via POST method and to arbitrary details of other user's Fortify projects via GET method.

Exploit-DB publication at https://www.exploit-db.com/exploits/45990 </br>

PacketStorm publication at https://packetstormsecurity.com/files/150771/Fortify-SSC-17.10-17.20-18.10-User-Detail-Insecure-Direct-Object-Reference.html

# Timeline
================</br>
2018-05-24: Discovered </br>
2018-05-25: Retest PRO environment </br>
2018-05-31: Vendor notification, two issues found  </br>
2018-05-31: Vendor feedback received </br>
2018-06-01: Internal communication </br>
2018-06-01: Vendor feedback, two issues are confirmed </br>
2018-06-05: Vendor notification, new issue found </br>
2018-06-06: Vendor feedback, evaluating High submission </br>
2018-06-08: Vendor feedback, High issue is confirmed </br>
2018-06-19: Researcher, reminder sent </br>
2018-06-22: Vendor feedback, summary of CVEs handled as official way </br>
2018-06-26: Vendor feedback, official Hotfix for High issue available to test </br>
2018-06-29: Researcher feedback </br>
2018-07-02: Researcher feedback </br>
2018-07-04: Researcher feedback, Hotfix tested on QA environment </br>
2018-07-05: Vendor feedback, fixes scheduled Aug/Sep 2018 </br>
2018-08-02: Reminder to vendor, feedback received OK! </br>
2018-09-26: Reminder to vendor, feedback received OK! </br>
2018-09-26: Fixes received from the vendor </br>
2018-10-02: Internal QA environment failed, re-building researcher 's ecosystem </br>
2018-10-11: Internal QA environment failed, re-building researcher 's ecosystem </br>
2018-10-11: Feedback from the vendor, technical details provided to the researcher </br>
2018-10-16: Fixes now tested on QA environment </br>
2018-11-08: Reminder received from the vendor, feedback provided by researcher </br>
2018-11-09: Re-rest fixes on QA environment </br>
2018-11-15: Re-rest fixes on QA environment now with SSC 18.20 version deployed </br>
2018-11-21: Researcher feedback </br>
2018-11-23: Fixes working well/confirmed by researcher </br>
2018-11-23: Vendor feedback, final details to disclosure the CVE and official fixes available for customers. </br>
2018-11-26: Vendor feedback, CVE, and official fixes to be disclosure </br>
2018-11-26: Agreements with the vendor to publish the CVE/Advisory.  </br>
2018-12-12: Public report </br>

# Microfocus (Fortify Product) Patch and credits: 
https://softwaresupport.softwaregrp.com/document/-/facetsearch/document/KM03298201

![vendor_patch_and_credits_12 12 18](https://user-images.githubusercontent.com/3140111/49884859-c6608d80-fe2d-11e8-8dcd-dfc17e9bd890.png)

# Author
Alex Hernandez aka <em><a href="https://twitter.com/_alt3kx_" rel="nofollow">(@\_alt3kx\_)</a></em><br>

My current exploit list @exploit-db: <br>
https://www.exploit-db.com/author/?a=1074 <br>
https://www.exploit-db.com/author/?a=9576 <br>

CVE-2018-7691 with sexy screens here: https://medium.com/@alt3kx
