# CVE-2020-12077
MapPress Maps Pro &lt; 2.53.9 - Remote Code Execution (RCE) due to Incorrect Access Control in AJAX Actions

### Description

The pro version of this plugin registers several AJAX actions that call functions which lack capability checks and nonce checks, specifically the ‘ajax_get’, ‘ajax_save’, and ‘ajax_delete’ functions in mappress_template.php. As such, it is possible for a logged-in attacker with minimal permissions, such as a subscriber, to perform the following actions:
Upload an executable PHP file (including potential backdoors) and achieve Remote Code Execution by sending a $_POST request to wp-admin/admin-ajax.php with the ‘action’ parameter set to ‘mapp_tpl_save’, the ‘name’ parameter set to the base name of the file they want to create, and the ‘content’ parameter set to executable PHP code. This file would then be created in and could be executed from the directory of the currently active theme.

Delete any existing PHP file on the site (such as wp-config.php) by sending a $_POST request to wp-admin/admin-ajax.php with the ‘action’ parameter’ set to ‘mapp_tpl_delete’, and the ‘name’ parameter set to the basename of the file to delete. For example, to delete wp-config.php a directory traversal attack could be used, and the ‘name’ parameter could be set to ‘../../../wp-config’). This would cause the site to be reset, at which point an attacker could gain full control of the site.

View the contents of any existing PHP file on the site (such as wp-config.php) by sending a $_GET request to wp-admin/admin-ajax.php with the ‘action’ parameter set to ‘mapp_tpl_get’, and the ‘name’ parameter of the file to disclose. For example, to view the contents of wp-config.php, a directory traversal attack could be used, and the ‘name’ parameter could be set to’../../../../wp-config’.


POC
---
```
python3 exploit.py --url http://wordpress.lan --username user --password useruser1 --code "<?php phpinfo(); ?>"
```
