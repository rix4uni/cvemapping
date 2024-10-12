# CVE-2022-29063: Java Deserialization via RMI Connection in Apache OfBiz

The OfBiz Solr plugin is configured by default to automatically make a RMI request on localhost, port 1099.
By hosting a malicious RMI server on localhost, an attacker may exploit this behavior, at server start-up or on a server restart, in order to run arbitrary code as the user that started OfBiz and potentially elevate his/her privileges.

### Vendor Disclosure:

The vendor's disclosure and fix for this vulnerability can be found [here](https://issues.apache.org/jira/browse/OFBIZ-12646).

### Requirements:

This vulnerability requires:
<br/>
- Run a malicious RMI server on localhost:1099
- Wait for Apache OfBiz application to start/restart

### Proof Of Concept:

More details and the exploitation process can be found in this [PDF](https://github.com/mbadanoiu/CVE-2022-29063/blob/main/Apache%20OfBiz%20-%20CVE-2022-29063.pdf).
