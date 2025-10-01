# Dashy Auth bypass
Exploit Title: Dashy authentication bypass\
Date: 02.10.2025\
Vendor Homepage: [Dashy.to](https://dashy.to/)\
Version: 3.1.1\
Tested on: 3.1.1\
CVE: CVE-2025-57617

Default version of authentication can be bypassed. Config YAML file, containing users information, including login, password hash and hash algorithm for each user, including dashboard admin. Intercepting the response with this file using Burp Suite allows to tamper with hash and replace it with arbitrary value. It can be done with "Match and replace" tool in Burp suite. That way it's possible to replace hash with the hash of your password and simply use this password to login. By login as administrator it's possible to get control over dashboard and its content
