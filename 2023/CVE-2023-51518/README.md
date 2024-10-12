# CVE-2023-51518: Preauthenticated Java Deserialization via JMX in Apache James

Apache James distribution prior to release 3.7.5 and 3.8.1 allow privilege escalation via JMX pre-authentication deserialization. Given a deserialization gadget, this could be leveraged as part of an exploit chain that could result in privilege escalation.

<strong>Note:</strong> For Apache James servers running using Java versions <16, the [ysoserial](https://github.com/frohoff/ysoserial) "CommonsBeanutils1" gadget can be used to execute arbitrary system commands. For Java versions >=16, an alternative vector needs to be identified as explained in this [article](https://mogwailabs.de/en/blog/2023/04/look-mama-no-templatesimpl/).

### Vendor Disclosure:

The vendor's disclosure and fix for this vulnerability can be found [here](https://james.apache.org/server/feature-security.html).

### Proof Of Concept:

More details and the exploitation process can be found in this [PDF](https://github.com/mbadanoiu/CVE-2023-51518/blob/main/Apache%20James%20-%20CVE-2023-51518.pdf).
