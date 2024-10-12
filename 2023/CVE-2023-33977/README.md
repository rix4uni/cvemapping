# CVE-2023-33977

# Stored XSS Via SVG Upload in kiwitcms/kiwi - by M Nadeem Qazi

## Description

This repository addresses the stored XSS vulnerability discovered in the kiwitcms/kiwi application, which was assigned the CVE-2023-33977 identifier. The vulnerability allows for the execution of malicious scripts via SVG file uploads. When an SVG file containing the payload is uploaded, the script gets executed in the context of the victim's browser, potentially leading to data theft, account compromise, and the distribution of malware.

## Proof of Concept

A detailed proof of concept for this vulnerability can be found in the following video:

[![Proof of Concept](https://img.youtube.com/vi/73qXeC8vUFg/0.jpg)](https://www.youtube.com/watch?v=73qXeC8vUFg)

## Impact

The impact of this vulnerability is significant and poses a serious risk to the security and integrity of the kiwitcms/kiwi application. Attackers can leverage this vulnerability to inject malicious scripts into the website, potentially allowing them to steal sensitive information, hijack user sessions, deface the website, manipulate content, and launch phishing attacks. These actions can result in reputational damage, compromised user accounts, and the dissemination of malware throughout the system.

## References

For more details on this vulnerability, please refer to the following resources:

- [huntr.dev Report](https://huntr.dev/bounties/19470f0b-7094-4339-8d4a-4b5570b54716/)
- [Medium Blog - Stored XSS Via SVG Upload in kiwitcms/kiwi]([https://medium.com/@mnqazi/stored-xss-vulnerability-in-kiwitcms-kiwi-cve-2023-33977-1234567890](https://medium.com/@mnqazi/cve-2023-33977-unrestriced-file-upload-leads-to-stored-xss-in-kiwitcms-12-4-m-nadeem-qazi-29a34dd2cbb7))

You can also follow me for updates on my research and other security-related topics:

- Instagram: [@mnqazi](https://www.instagram.com/mnqazi)
- Twitter: [@mnqazi](https://twitter.com/mnqazi)
- Facebook: [@mnqazi](https://www.facebook.com/mnqazi)
- LinkedIn: [M Nadeem Qazi](https://www.linkedin.com/in/m-nadeem-qazi)

Let's prioritize security and protect our systems from potential threats. Stay vigilant! 💻🔒
