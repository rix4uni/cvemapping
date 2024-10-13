# CVE-2018-12086 PoC

https://nvd.nist.gov/vuln/detail/CVE-2018-12086

https://opcfoundation.org/SecurityBulletins/OPC%20Foundation%20Security%20Bulletin%20CVE-2018-12086.pdf

TL;DR: some OPC UA stacks are vulnerable to a stack overflow when decoding specially crafted requests.

## Build

`mvn clean package`

## Run

`java -jar target/stack-overflow-poc.jar <endpointUrl>` 
