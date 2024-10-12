# CKEditor cross-site scripting vulnerability in AJAX sample
CVE-2023-4771 PoC CKEditor 4 Cross-site scripting (XSS) vulnerability in AJAX sample

This document describes how to perform an XSS vulnerability (CVE-2023-4771) using CKEditor. 
Make sure the following is done with great caution to follow through:

Prerequisite

• Have access to a CKEditor instance. 

File: ckeditor/samples/old/ajax.html.

Steps to perform the XSS Vulnerability:

Visit CKEditor Sample Page
Open your favorite browser and visit this URL: /ckeditor/samples/old/ajax.html. This URL should point to the CKEditor sample page, which resides on the tested web application.

Create a New Editor Instance:
Go to the CKEditor sample page and thus find there any control - button, link, etc., that allows you to create a new editor instance; click it. The CKEditor instance on the page should be activated.

Switch to Source Mode:
If the CKEditor instance is ready, find and click the "Source" button. This button allows you to control the raw HTML content in the editor.

Inject the XSS Payload:
In the source view, a textarea is given where you can write in HTML code. The following is an example of such an XSS payload that you would like to inject into this textarea:

```js
<p>Xss<!-- --!><img src=1 onerror=alert(`XSS`)>-->Attack</p>
```

The payload is logic that should raise an alert in rendering this HTML.

Remove Editor Instance:
After the pasting of the payload, seek the button/link entitled "Remove Editor" and click on it. This will turn off the CKEditor instance and output the content in HTML.

Observe the XSS Alert:
If the application is vulnerable, after the editor is removed and the content in HTML is rendered, an alert box with the message "XSS" appears.

Vulnerable code in ajax.html: document.getElementById( 'editorcontents' ).innerHTML = html = editor.getData();

![alt text](https://raw.githubusercontent.com/sahar042/CVE-2023-4771/main/Vulnerable.png)
![alt text](https://raw.githubusercontent.com/sahar042/CVE-2023-4771/main/Vulnerable%232.png)
![alt text](https://raw.githubusercontent.com/sahar042/CVE-2023-4771/main/Vulnerable%233.png)

References:

• https://cve.mitre.org/cgi-bin/cvename.cgi?name=2023-4771

• https://github.com/ckeditor/ckeditor4/commit/8ed1a3c93d0ae5f49f4ecff5738ab8a2972194cb#diff-9dac7a5ea2ec534d0c2f459c2d6dceae37b849cf9c7210b43a6e74b2d82ad3ba

Credit for the PoC: Sahar Shlichove

Credit for the CVE report: Rafael Pedrero
