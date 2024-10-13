# CVE-2021-40906 - Reflected XSS in an unauthenticated zone

**Application:** CheckMK Management Web Console

**Software Revision:** From 1.5.0 to 1.5.0p25

**Author:** Edgar Augusto Loyola Torres.

**Attack type:** Reflected XSS

**Solution:** Update to Software Revision 1.6.0p26 or later

**Summary:** CheckMK Raw Edition software (versions 1.5.0 to 1.6.0) does not sanitise the input of a web service parameter that is in an unauthenticated zone. This Reflected XSS allows an attacker to open a backdoor on the device with HTML content and interpreted by the browser (such as JavaScript or other client-side scripts) or to steal the session cookies of a user who has previously authenticated via a man in the middle. Successful exploitation requires access to the web service resource without authentication.

**Technical Description:** See CVE-2021-40906

**Timeline:**
   * 2021-09-01 Issues discovered.
   * 2021-09-06 First contact with vendor via e-mail.
   * 2021-09-08 Vendor response. XSS vulnerabilities were already detected, and would be patched in the next release.
   * 2021-09-30 New Software Version release(1.6.0p27) and Vulnerability patch confirmed.
  

**Reference:**
   * https://checkmk.com/werk/13192
   * https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-40906
   * https://nvd.nist.gov/vuln/detail/CVE-2021-40906

# DEMO
  **PoC CheckMk version 1.5.0p25 Raw Edition**
  
![Reflected XSS](https://raw.githubusercontent.com/Edgarloyola/CheckMK_Reflected_XSS/main/XSS_no_auth.png?token=AKM5DALLSIBJD5HXANVKUULBMVMTG)
