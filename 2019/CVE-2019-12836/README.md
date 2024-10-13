# CVE-2019-12836

![bobronix](https://github.com/9lyph/CVE-2019-12836/assets/44860700/a3f87ea7-b1bb-44ca-8f95-b2bbcf10dc59)

#### Application

JEditor v3.0.5 - WYSIWIG Editor for JIRA

Simple yet powerful rich text editor for Jira. Import HTML emails, paste rich contents, create templates and prepopulate fields.

#### Vendor of Product

Bobronix

#### Vendor Website

http://bobronix.com/

#### CVE Reference

[https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2019-12836](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2019-12836)

#### Affected Product Code Base

JEditor - WYSIWYG Editor for Jira - v3.0.5

#### Affected Component

JEditor v3.0.5

#### Description

The Bobronix JEditor editor before v3.0.6 for Jira allows an attacker to add a URL/Link (to an existing issue) that can cause forgery of a request to an out-of-origin domain.  This in turn may allow for a forged request that can be invoked in the context of an authenticated user, leading to stealing of session tokens and account takeover.

JEditor v3.0.5 allows for upload of files of various file extension types, one of which is '.HTML'. JEditor is utilised by JIRA for its file upload functionality. Using this functionality an attacker is able to upload malicious content.

Once the malicious content is uploaded a subsequent request can be made for the content which allows for the inline displaying and rendering of the content within the context of any authenticated user's browser. This may allow for an attacker to forge a  malicious request, on behalf of any authenticated user. 

#### Vulnerability Type

Cross Site Request Forgery (CSRF)

#### Additional Information

Bug Fixed in JEditor v3.0.6

https://jeditor.zendesk.com/hc/en-us/articles/360029430751-JEditor-3-0-6-release-notes

#### CVE Impact Other

Allows for a forged request resulting in a client side attack vector possibility

#### Attack Vectors

Authenticated user required to interact with the embedded link/URL

#### Discoverer

Credit: Victor Hanna (Exploit Security)

#### POC

##### Example HTTP Request

```
GET /plugins/servlet/jeditor_file_provider?imgId=ckupload201906162566696393384747423&fileName=C%3A%5Ctemp%5CPOC.html HTTP/1.1
Host: <vulnerable host>
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0)
Accept: text/html,application/xhtml_xml,application/xml;q=0.9,*/*;q=0.8
Accept-Langauge: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: https://<vulnerable host>/secure/Dashboard.jspa
DNT: 1
Connection: close
Cookie: atlassian.xsrf.token=BNXD-VY4I-RCJA-J3YA_34d13dd7fae0f32023fc89838ldc0b6c35991382_lin; JSESSION=42E9F5581BAE499E3E9E45B9D44E6F3C
Upgrade-Insecure-Requests: 1
```

##### Example HTTP Response

```
HTTP/1.1 200
Server: nginx/1.10.2
Date: Sun, 16 Jun 2019 03:06:10 GMT
Content-Type: text/html;charset=UTF-8
Connection: close
X-AREQUESTID: 786x226666x1
X-ASESSIONID: pn6xpm
X-XSS-Protection: 1; mode=block
X-Content-Type-Options: nosniff
X-ASEN: SEN-2322842
X-Seraph-LoginReason: OK
X-AUSERNAME:
Content-Disposition: inline; filename="C:\temp\POC.html"
Vary: User-Agent
Content-Length: 236

<html>
<head>
<img src="http://{insert external image location here}">
<script>{JS Payload of any description}</script>
</head>
<body>
<h1>
 Welcome to the Jungle !
</h1>
</body>
</html>
```

#### Discoverer/Credit
Victor Hanna of Exploit Security

#### Follow me on
<a rel="me" href="https://defcon.social/@9lyph">Mastodon</a> [Linkedin](https://www.linkedin.com/in/victor-h-a894a84/) [Youtube](https://www.youtube.com/channel/UC79Q2b0tHeqsjjvEH0k7jZw)
