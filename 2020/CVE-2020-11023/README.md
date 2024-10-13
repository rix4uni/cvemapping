
# CVE-2020-11023 POC Dom XSS
This proof of concept, demostraste an security flaw of dom-bases XSS manipulating and using JQuery DOM Methods. eg:(.append, .text,.html)


Payload i used:
alert("Text: " + $("#test").text());


To test the vulnerability do the following:

1. Open and web console, on your browser and in the scope site.

2. Go to the console window and put the following payload:

3. Payload: 
alert("Text: " + $("#test").text());
