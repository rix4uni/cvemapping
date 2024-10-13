# CVE-2021-40905 - RCE via a crafted .mkp file

**Application:** CheckMK Management Web Console

**Software Revision:** Less than or equal to 2.0.0p17

**Attack type:** RCE

**Solution:** TBD or the MKPs shared on [https://exchange.checkmk.com/] are manually reviewed by CheckMk and they look for malicious code or suspicious imports, etc.

**Summary:** The web management console of CheckMk Enterprise Edition (versions 1.5.0 to 2.0.0p17) does not properly sanitise the uploading of ".mkp" files which are Extension Packages, making remote code execution possible. Successful exploitation requires access to the web management interface, either with valid credentials or with a hijacked session of a user with administrator role.

**Technical Description:** See CVE-2021-40905

**Timeline:**
   * 2021-09-01 Issues discovered.
   * 2021-09-06 First contact with vendor via e-mail.
   * 2021-09-08 Vendor response. RCE vulnerabilities were already detected, and would be patched in the next release.
   * 2022-03-25 Public disclosure.
  

**Reference:**
   * https://exchange.checkmk.com/
   * http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-40905
   * https://nvd.nist.gov/vuln/detail/CVE-2021-40905


