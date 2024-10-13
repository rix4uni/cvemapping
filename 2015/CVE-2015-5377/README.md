# CVE-2015-5377
Elasticsearch 1.5.2 is vulnerable to RCE through insecure java deserialization.

The exploit attack the transport protocol on port 9300. The deserialization is based on Groovy MethodClosure chain to achive RCE.
