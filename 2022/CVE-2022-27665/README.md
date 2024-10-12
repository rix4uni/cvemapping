# CVE-2022-27665
A Reflected XSS via AngularJS Sandbox Escape Expressions vulnerability exists in Progress/IPSwitch WS_FTP Server 8.6.0 that can lead to execution of malicious code and commands on the client due to improper handling of user provided input. By inputting malicious payloads in the subdirectory searchbar or Add folder filename boxes, it is possible to execute client-side commands.

This vulnerability is also known as a Client-Side Template Injection, and is similar to Server-Side Template Injections. 


<p align="center">
  <img src="https://github.com/dievus/CVE-2022-27665/blob/main/images/malinput.png" />
</p>

<p align="center">
  <img src="https://github.com/dievus/CVE-2022-27665/blob/main/images/burpinspect.png" />
</p>

<p align="center">
  <img src="https://github.com/dievus/CVE-2022-27665/blob/main/images/maloutput.png" />
</p>

**Vulnerability Timeline**

|      Date      |      Action      |
| -------------- | ---------------- |
| 3/22/2022      | Vulnerability discovered |
| 3/22/2022      | Vulnerability disclosed to vendor |
| 3/22/2022      | CVE ID Requested via MITRE |
| 3/22/2022      | Vendor requested resubmission via HackerOne |
| 3/23/2022      | MITRE reserved CVE ID | 
| 3/23/2022      | HackerOne accepted submission | 
| 3/30/2022      | Vulnerability acknowledged by vendor and set to triaged by H1 |
| 4/03/2023      | Vulnerability disclosed and CVE made public | 

https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-27665

