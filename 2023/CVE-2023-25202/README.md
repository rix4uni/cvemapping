# CVE-2023-25202: Insecure file upload mechanism

![image](https://github.com/Trackflaw/CVE-2023-25202/assets/78696986/43469252-55f4-422a-aef5-c5805e8eccf2)

## Description

CVE-2023-25202 involves an insecure file upload mechanism within the Therefore application, which is overly permissive in the types of files users can upload. The application only blocks uploads of HTML, EXE, and BAK files, leaving it vulnerable to uploads of technical files like PHP, ASP, ASPX, and JSP. These file types could potentially allow system command execution under certain conditions, although not exploitable in this context.

The application's safeguard against HTML file uploads can be circumvented by uploading markdown files that support HTML, exposing the system to risks without allowing the upload of directly executable files like malware. This vulnerability opens the door for attackers to exploit Server-Side Request Forgery (SSRF) vulnerabilities, upload malicious files (excluding executable types), or initiate denial-of-service attacks. In some scenarios, attackers could execute code through the uploaded files.

To mitigate these risks, it is recommended to restrict the range of permissible file types to those strictly necessary, primarily focusing on text processing documents (such as Office and PDF files) and images. Limiting the number of allowed extensions, with guidance from the extensions supported by the Aspose plugin developer, can help protect against such vulnerabilities.

## CVE details

- **Affected product** : CVE-2023-25202 affected `Therefore Case Manager 2018/2021` and `Therefore Solution Designer 2018/2021`
- **Affected version** : All the versions equal or lower at `18.4.0` and equal or lower at `26.1.1`  are vulnerable to CVE-2023-25202.
- **CVE ID** : CVE-2023-25202.

## More informations

https://blog.trackflaw.com/en/multinational-hacking-with-file-upload-and-ssrf/
