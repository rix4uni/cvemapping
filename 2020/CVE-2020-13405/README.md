# CVE-2020-13405

- Base Score:  7.5 HIGH🟥

MicroWeber is an open-source Content Management System (CMS) written in PHP. It allows web administrators to easily build a website by dragging and dropping components where they want them to be. It is a popular choice among those looking to start a website that is both easy to set up and is very customizable.

`userfiles/modules/users/controller/controller.php` in Microweber before `1.1.20` allows an unauthenticated user to disclose the users database via a `/modules/` `POST` request. 

When an attacker sends a POST request to this endpoint, it leads to the unauthorized disclosure of sensitive user information, including usernames, passwords, and email addresses, from the users' database. 

![image](https://github.com/mrnazu/CVE-2020-13405/assets/108541991/6cff8df6-6289-442e-8be1-f7edd62b0f23)

As a PHP-centric Content Management System, MicroWeber engages a variety of PHP scripts to manage its diverse functionalities. This inherent design enables MicroWeber to be highly adaptable, empowering users to seamlessly integrate their own scripts or effortlessly tweak existing ones, thereby offering a means to tailor the operation of the CMS according to individual preferences.

The vulnerability was discovered in the “controller.php” script, which is part of MicroWeber’s users module.
```php
<?php
dd(User::all());
```
This code snippet reveals the presence of a serious security vulnerability in the `"controller.php"` script of MicroWeber's users module. The code `dd(User::all());` suggests that it's attempting to dump and display all user records from the database using the `User::all()` method.


## PoC
Now, once you have saved the PoC from here, then.. you need to open up your terminal and start a python server: `python -m SimpleHTTPServer 4444`
Now, Go to your browser and load it.

Enjoy! Use censys search engine to find a target with a version before `1.1.20`
