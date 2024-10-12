# CVE-2022-45472
<br>DOM Based XSS</br>
<br>Software: CAE Learning Space Enterprise with Intuity License </br>
<br>Image Version: 267r </br>
<br>Patch Level: 639 </br>
<br>Vulnerability: DOM Based XSS </br>

## Description
The CAE Learning Space Enterprise management software is vulnerable to a DOM Based XSS attack. A DOM Based XSS attack is when a user sends an executed payload to the host and as a result, it modifies the DOM environment in the victim's browser from the original client-side script. This attack was found through manually searching burp requests, running tested parameters through a XSS finder tool called Dalfox (https://github.com/hahwul/dalfox), then verifying the DOM of the affected host to view the behavior of the application. 

## Impact
An attacker can insert malicious code within the application DOM. This code can be executed causing the application to run client code unexpectedly. For testing purposes, the impact showed a payload consisting of a basic alert being called within the DOM inspection from the “ontouchmove” and “onpointerup” JavaScript functions. Then after sending the payload, the tester could see within the DOM itself the break of the “value” html value and then the JavaScript function itself.  

## Recommendation 
To prevent DOM XSS, you must sanitize all untrusted data, even if it is only used in client-side scripts. If you must use user input on your page, always use it in the text context, never as HTML tags or any other potential code. If you can, entirely avoid using user input, especially if it affects DOM elements. 

## Reproduction Steps
Download the CVE word doc to see the attack path with screenshots.
