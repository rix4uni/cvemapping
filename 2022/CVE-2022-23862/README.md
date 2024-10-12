# CVE-2022-23862: Local Privilege Escalation via Unauthenticated JMX in YSoft SafeQ

The SafeQ JMX service running on port 9696 is vulnerable to JMX MLet attacks. Because the service did not enforce authentication and was running under the “NT Authority\System” user, we were able to use the vulnerability to execute arbitrary code and elevate to the system user.

### NVD Disclosure:

The disclosure for this vulnerability can be found [here](https://nvd.nist.gov/vuln/detail/CVE-2022-23862).

### Requirements:

This vulnerability requires:
<br/>
- Access to TCP port 9696

### Proof Of Concept:

More details and the exploitation process can be found in this [PDF](https://github.com/mbadanoiu/CVE-2022-23862/blob/main/SafeQ%20-%20CVE-2022-23862.pdf).
