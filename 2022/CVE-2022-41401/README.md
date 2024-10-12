# OpenRefine <= v3.5.2 SSRF

[OpenRefine](https://github.com/OpenRefine/OpenRefine) v<=3.5.2 contains a Server-Side Request Forgery (SSRF) vulnerability, which permits unauthorized users to exploit the system, potentially leading to unauthorized access to internal resources and sensitive file disclosure.

The root cause of this vulnerability lies in OpenRefine's inadequate server-side validation of the supplied URL. While client-side validation exists, the server-side fails to perform the same level of scrutiny. Consequently, if a user initially provides a valid URI and then later substitutes it with a malicious one, the server-side system fails to detect the alteration.

# PoC 

This vulnerability can be leveraged during the process of creating a new project in OpenRefine. Specifically, by selecting the option to import a project from Web Addresses URLs, a malicious actor can insert a payload that enables them to access internal resources or read sensitive files.


![image](https://github.com/ixSly/CVE-2022-41401/assets/32583633/4d71ef1f-2f02-4b48-8c45-5be99f4f0433)


![image](https://github.com/ixSly/CVE-2022-41401/assets/32583633/df914755-f5eb-43d6-9638-ccdb5d8cb0c3)



# Disclosure Timeline

- Date of Discovery: 10/04/2022
- Reported to OpenRefine Security Team: 15/04/2022
- OpenRefine Team Acknowledgment: 23/05/2022
- Security Path Release: 07/07/2022
