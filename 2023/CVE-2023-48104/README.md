# CVE-2023-48104
HTML Injection in Alinto/SOGo Web Client

## Vendor of Product
Alinto

## Vulnerability Type
HTML Injection

## Affected Versions
SOGo Web Mail < 5.9.1

## Attack Vectors
Phishing - In the body of the message, you can inject a malicious form that will send the entered data to the attacker.

## Additional Information
The fix to prevent form tag in mail body has been made -> https://github.com/Alinto/sogo/commit/7481ccf37087c3f456d7e5a844da01d0f8883098

## Discoverer
Spiridonov Ivan/E1tex

## PoC
For demonstration purposes only. PoC Exploit works on SOGo vulnerable clients.
