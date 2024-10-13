struts1filter
=============

A request parameter filter solution for [Apache Struts 1](http://struts.apache.org/) [CVE-2014-0114](https://issues.apache.org/jira/browse/STR-3220) based on the work of [Alvaro Munoz and the HP Fortify team](http://h30499.www3.hp.com/t5/HP-Security-Research-Blog/Protect-your-Struts1-applications/ba-p/6463188#.VDqkCdTLeT4).

To use this filter, add the following filter declaration along with appropriate mapping to the web.xml descriptor
of the Apache Struts 1 application to protect:

```
<filter>
    <filter-name>ParamWrapperFilter</filter-name>
    <filter-class>net.rgielen.struts1.filter.ParamWrapperFilter</filter-class>
</filter>
<filter-mapping>
    <filter-name>ParamWrapperFilter</filter-name>
    <servlet-name>YOUR ACTION SERVLET</servlet-name>
</filter-mapping>
```

The filter comes with a default regular expression to match harmful parameter names,
 which might be overridden by explicit configuration:
 
```
<filter>
    <filter-name>ParamWrapperFilter</filter-name>
    <filter-class>net.rgielen.struts1.filter.ParamWrapperFilter</filter-class>
    <init-param>
        <param-name>excludeParams</param-name>
        <param-value>(.*\.|^|.*|\[('|"))(c|C)lass(\.|('|")]|\[).*</param-value>
    </init-param>
</filter>
...
```

The filter is released Maven Central. Use the following Maven dependency declaration to incorporate it in your project
(Ivy, Gradle and SBT accordingly):
```
<dependency>
    <groupId>net.rgielen</groupId>
    <artifactId>struts1filter</artifactId>
    <version>1.0.0</version>
</dependency>
```
It can also be downloaded directly. Use [the Central Repository Search](http://search.maven.org/) with the coordinates
provided above to find and download the jar.
