# CVE-2024-42758

A Cross-site Scripting (XSS) vulnerability exists in version v2024-01-05 of the indexmenu plugin when is used and enabled in Dokuwiki (Open Source Wiki Engine). A malicious attacker can input XSS payloads for example when creating or editing existing page, to trigger the XSS on Dokuwiki, which is then stored in .txt file (due to nature of how Dokuwiki is designed), which presents stored XSS.

https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2024-42758

Vulnerable Dokuwiki page: doku.php?id=[page_name]

Vulnerable Payload: <script>alert('XSS')</script>

![image](https://github.com/user-attachments/assets/beeed529-c5f8-4d14-83b7-55e4df07a83a)

![image](https://github.com/user-attachments/assets/e3895d64-8f2b-4b86-ae44-275c9b315213)

![image](https://github.com/user-attachments/assets/a791fd07-a848-4c07-a9ae-99bf2c525429)

Discovered by Antun Matija Kriskovic, July 2024
