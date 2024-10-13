# CVE-2020-8825

<p align="center">
    <img src="https://github.com/hacky1997/CVE-2020-8825/blob/master/cve.jpg" alt = "cve">
</p>
   
## Publish:
  [CVE-2020-8825](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-8825)

## Vendor:
    PHP VanillaForum 

## Description:   
    The vulnerability exists due to insufficient sanitization of user-supplied data passed to "index.php?p=/dashboard/settings/branding" URL. A remote attacker can permanently inject and execute arbitrary HTML and script code in user's browser in context of vulnerable website.
    Successful exploitation of this vulnerability may allow a remote attacker to steal potentially sensitive information, change appearance of the web page, perform phishing and drive-by-download attacks.

## Environment:

    Version: 2.6.3
    OS: Windows 10, Linux
    PHP: 7
    URL: index.php?p=/dashboard/settings/branding
       
## Proof of Concept:
  <p align="center">
    <img src="https://github.com/hacky1997/CVE-2020-8825/blob/master/vanilla.png" alt="vanilla">
  </p>

## Assigned by:
  [Sayak Naskar](https://github.com/hacky1997/)
  

