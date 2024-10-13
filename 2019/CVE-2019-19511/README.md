# CVE-2019-19511
Chevereto - 1.0.0 Free - 1.1.4 Free, <= 3.13.4 Core, Remote Code Execution

# Description
installer.php in Chevereto through 1.1.4 Free, and through 3.13.4 Core, allows remote authenticated admins to execute arbitrary PHP code by injecting this code into the setup process and overwriting the settings.php file, which will then contain the injected code. Since settings.php is overwritten, it also resets the application and puts it in a denial of service state until the settings are restored.

# Reference
https://github.com/Chevereto/Chevereto-Free/blob/1.1.4/app/install/installer.php#L736
