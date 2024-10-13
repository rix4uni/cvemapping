ElasticSearch search Remote Code Execution (CVE-2014-3120)
===========================

POC Code to exploit CVE-2014-3120

Requirements: python

Usage: python elastic_check.py <file in host:port format>

Example:
```
➜ ~$ python elastic_check.py hostport.txt
0	10.0.0.10:9200	Vulnerable
1	10.0.0.11:9201	Not Vulnerable
2	10.0.0.12:9201	Connection error

Vulnerable hosts: 1
Not-vulnerable hosts: 1
Connection Errors: 1
```

hostport.txt:
```
10.0.0.10:9200
10.0.0.11:9201
10.0.0.12:9201
```
