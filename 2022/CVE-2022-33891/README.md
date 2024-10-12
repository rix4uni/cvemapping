# CVE-2022-33891 - Apache Spark UI Remote Code Execution (RCE) 🔐

Apache Spark UI is susceptible to a remote command injection vulnerability identified as CVE-2022-33891. This flaw arises due to improper handling of user authentication and access control, specifically when Access Control Lists (ACLs) are enabled. With ACLs activated through the `spark.acls.enable` configuration option, an authentication filter is supposed to validate whether a user has the necessary permissions to view or modify the application. However, a vulnerability exists within the `HttpSecurityFilter` that allows for impersonation by supplying an arbitrary username.

## Vulnerability Details 🛠

When ACLs are enabled, a specific code path within `HttpSecurityFilter` fails to adequately verify user identities. This oversight permits an attacker to bypass the authentication mechanism and reach a permission check function. This function inadvertently constructs and executes a Unix shell command based on user-supplied input, leading to arbitrary code execution on the server hosting the Apache Spark UI.

### Affected Versions 🚨

The vulnerability impacts the following versions of Apache Spark:
- Versions 3.0.3 and earlier
- Versions 3.1.1 to 3.1.2
- Versions 3.2.0 to 3.2.1

## Proof of Concept (PoC) 💻

A Proof of Concept (PoC) has been developed to demonstrate the exploitability of this vulnerability. This PoC is intended strictly for educational and security research purposes, to aid in the understanding and mitigation of this flaw.

### Disclaimer ⚠️

The provided PoC is for educational and ethical hacking purposes only. Usage of the PoC for attacks against web applications or servers without prior mutual consent is illegal. The author assumes no liability and is not responsible for any misuse or damage caused by this material. Users are urged to use this information responsibly and ethically.
