# CVE-2024-34312

[![Product](https://img.shields.io/badge/product-Virtual%20Programming%20Lab%20for%20Moodle%20%3C4.2.4-orange?style=for-the-badge&logo=GitHub)](https://github.com/jcrodriguez-dis/moodle-mod_vpl)
[![CWE](https://img.shields.io/badge/CWE-80-%23f0f0f0?style=for-the-badge&logo=OWASP)](https://cwe.mitre.org/data/definitions/80.html)

Description
---
[Virtual Programming Lab for Moodle](https://vpl.dis.ulpgc.es/) **up to v4.2.3** was discovered to contain a **Cross-Site Scripting (XSS)** vulnerability via its **IDE component**.

Additional Details
---
The browser connects directly to a websocket running on the jail server.
Through the websocket, the jail server can send messages directly to the browser. These messages are parsed by the browser and handled by "executionActions".
The "run:browser" action is vulnerable to XSS due to concatenating HTML with untrusted input and injecting it into the page body.
This can be abused by a compromised jail server to gain administrative access on the moodle instance through XSS.

Exploitation
---
An attacker controlling the untrusted jail server, can install a malicious jail server which sends a malicious payload to any user, using the Virtual Programming Lab, triggering XSS.

An example payload would look like this: `run:browser:test\">test</a><script>alert(1)</script><a href=\"test\"`. This would result in `<script>alert(1)</script>` being included in the DOM causing `alert(1)` to be executed.

![image](https://github.com/vincentscode/CVE-2024-34312/assets/26576880/153b7d26-975c-4282-87fd-da961a6f3c55)


The vulnerable code in `vplide.js` interprets this as a command and appends its second argument (arguments are seperated by `:`) to the dom directly:
```js
executionActions = {
    // ...
    'run': function(content, coninfo, ws) {
        var parsed = /^([^:]*):?(.*)/i.exec(content);
        var type = parsed[1];
        if (type == 'terminal' || type == 'webterminal') {
            // ...
        } else if (type == 'vnc') {
            // ...
        } else if (type == "browser") {
            var URL = (coninfo.secure ? "https" : "http") + "://" + coninfo.server + ":" + coninfo.portToUse + "/";
            URL += parsed[2] + "/httpPassthrough";
            if (isTeacher) {
                URL += "?private";
            }
            var message = '<a href="' + URL + '" target="_blank">';
            message += VPLUtil.str('open') + '</a>';
            var options = {
                width: 200,
                icon: 'run',
                title: VPLUtil.str('run'),
            };
            showMessage(message, options);
        } else {
            // ...
        }
    },
    // ...
}
```

Patch
---
```patch
diff --git a/amd/src/vplide.js b/amd/src/vplide.js
index 586b5ff5..d1f88f47 100644
--- a/amd/src/vplide.js
+++ b/amd/src/vplide.js
@@ -2024,8 +2024,8 @@ define(
                 'setResult': self.setResult,
                 'ajaxurl': options.ajaxurl,
                 'run': function(content, coninfo, ws) {
-                    var parsed = /^([^:]*):?(.*)/i.exec(content);
-                    var type = parsed[1];
+                    var parsed = /^([^:]*):?(.*)/.exec(content);
+                    var type = VPLUtil.sanitizeText(parsed[1]);
                     if (type == 'terminal' || type == 'webterminal') {
                         if (lastConsole && lastConsole.isOpen()) {
                             lastConsole.close();
@@ -2055,7 +2055,7 @@ define(
                                 });
                     } else if (type == "browser") {
                         var URL = (coninfo.secure ? "https" : "http") + "://" + coninfo.server + ":" + coninfo.portToUse + "/";
-                        URL += parsed[2] + "/httpPassthrough";
+                        URL += VPLUtil.sanitizeText(parsed[2]) + "/httpPassthrough";
                         if (isTeacher) {
                             URL += "?private";
                         }
diff --git a/amd/src/vplui.js b/amd/src/vplui.js
index 36504a33..648472d6 100644
--- a/amd/src/vplui.js
+++ b/amd/src/vplui.js
@@ -582,8 +582,8 @@ define(
             var messageActions = {
                 'message': function(content) {
                     var parsed = /^([^:]*):?([^]*)/.exec(content);
-                    var state = parsed[1];
-                    var detail = parsed[2];
+                    var state = VPLUtil.sanitizeText(parsed[1]);
+                    var detail = VPLUtil.sanitizeText(parsed[2]);
                     if (state == 'running') {
                         state = running;
                     }
@@ -607,7 +607,7 @@ define(
                     }
                 },
                 'retrieve': function() {
-                    var data = {"processid": VPLUtil.getProcessId()};
+                    var data = {"processid": coninfo.processid};
                     pb.close();
                     delegated = true;
                     VPLUI.requestAction('retrieve', '', data, externalActions.ajaxurl)
@@ -627,7 +627,7 @@ define(
                 'close': function() {
                     VPLUtil.log('ws close message from jail');
                     ws.close();
-                    var data = {"processid": VPLUtil.getProcessId()};
+                    var data = {"processid": coninfo.processid};
                     VPLUI.requestAction('cancel', '', data, externalActions.ajaxurl, true);
                 }
             };
```

References
---
* **CVE Record**: https://www.cve.org/CVERecord?id=CVE-2024-34312
* **Vendor URL**: https://vpl.dis.ulpgc.es/
* **Fixed Release**: https://github.com/jcrodriguez-dis/moodle-mod_vpl/releases/tag/V4.2.4
* **Commit**: https://github.com/jcrodriguez-dis/moodle-mod_vpl/commit/5faaaf1d01c4088d7c8e3b170dd57c84341cf695
* **CWE**: https://cwe.mitre.org/data/definitions/80.html
