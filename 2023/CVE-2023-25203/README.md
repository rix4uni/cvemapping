# CVE-2023-25203: Application vulnerable to SSRF (Server Side Request Forgery) attacks

![image](https://github.com/Trackflaw/CVE-2023-25203/assets/78696986/851d6bf7-0e37-498d-b776-ff19dd48da33)

## Description

CVE-2023-25203 identifies a vulnerability within the Therefore solution, which is susceptible to Server-Side Request Forgery (SSRF) attacks due to its use of Aspose software for converting uploaded files into PDF format. This software's capability to handle a wide range of file types introduces a risk when the application fails to adequately filter out unnecessary extensions.

Aspose, the software developer, has emphasized the importance of security measures to prevent servers from executing internal requests, which are the basis of SSRF attacks. The vulnerability in the Therefore solution enables several exploitation methods:

1. **Access to remote resources**: Demonstrated through the use of an SVG file, an attacker can make the application perform an HTTP GET request to a server under their control.
2. **Password hash retrieval**: In Windows environments, exploiting this SSRF vulnerability can redirect requests to an attacker's SMB server, capturing the NetNTLMv2 hash of the service account used by the application.
3. **Internal network mapping**: The vulnerability allows an attacker to map the internal network structure of the client, potentially using the victim machine as a proxy.

Additional potential exploits include port scanning, file reading (though Aspose seems to offer some protection against this), and initiating denial-of-service attacks by uploading documents with references to large images, thereby consuming significant system resources.

The primary risks posed by this vulnerability include credential theft, the disclosure of sensitive information through image files, mapping of the victim's information system infrastructure, and causing denial of service.

To mitigate these risks, adjustments to the Aspose plugin's configuration, which is used for file analysis, can prevent SSRF attacks. Aspose has already issued warnings about the dangers of loading remote elements, suggesting that awareness and proactive measures are essential for maintaining security.

## CVE details

- **Affected product** : CVE-2023-25203 affected `Therefore Case Manager 2018/2021` and `Therefore Solution Designer 2018/2021`
- **Affected version** : All the versions equal or lower at `18.4.0` and equal or lower at `26.1.1`  are vulnerable to CVE-2023-25203.
- **CVE ID** : CVE-2023-25203.

## More informations

https://blog.trackflaw.com/en/multinational-hacking-with-file-upload-and-ssrf/
