# Detection-and-Mitigation-script-for-CVE-2021-42717
Detection and Mitigation script for CVE-2021-42717 -> ModSecurity DoS Vulnerability in JSON Parsing 

ModSecurity 3.x through 3.0.5 mishandles excessively nested JSON objects. Crafted JSON objects with nesting tens-of-thousands deep could result in the web server being unable to service legitimate requests. Even a moderately large (e.g., 300KB) HTTP request can occupy one of the limited NGINX worker processes for minutes and consume almost all of the available CPU on the machine. Modsecurity 2 is similarly vulnerable: the affected versions include 2.8.0 through 2.9.4.

Possible Mitigation:  Create a phase:1 chained rule that will reject requests that would use the JSON parser if the Content-Length exceeds a certain size (10,000 to 20,000 bytes is likely safe in most installations).  Some v2 users may alternatively be able to make use of the SecRequestBodyNoFilesLimit configuration item if other non-file request bodies are likewise expected to be below similar thresholds. Special note to users with ModSecurity <v2.9.3:  although the problem exists in earlier versions like v2.9.2, it appears to require a larger request body size to trigger problematic delays, which means that limits involving the request body size can probably be larger (perhaps 40,000 to 50,000 bytes) and still provide decent protection in most installations.
https://www.trustwave.com/en-us/resources/blogs/spiderlabs-blog/modsecurity-dos-vulnerability-in-json-parsing-cve-2021-42717/


![image](https://user-images.githubusercontent.com/106553324/202918682-b9ff8b41-788e-4df9-8624-87ee288fa03e.png)
