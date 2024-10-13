# CVE-2019-10392_EXP
Jenkins Git Client Authenticated RCE CVE-2019-10392_Exp

## Usage
```
usage: Jenkins Git Client < 2.8.2. [-h] -u TARGET [-U USERNAME] [-P PASSWORD]
                                   [-i ITEM] [-I INTERACTIVE] [-c COMMAND]

optional arguments:
  -h, --help            show this help message and exit
  -u TARGET, --target TARGET
                        Target.
  -U USERNAME, --username USERNAME
                        This vulnerability need Jenkins username to login.
                        Default: admin
  -P PASSWORD, --password PASSWORD
                        This vulnerability need Jenkins password to login.
                        Default: admin
  -i ITEM, --item ITEM  Jenkins program Name to establish.
  -I INTERACTIVE, --interactive INTERACTIVE
                        Choose if you need a interactive shell(True or False).
                        Default: False
  -c COMMAND, --command COMMAND
                        Command to execute. If not use interactive mode it's
                        required.
```

## Reference
https://iwantmore.pizza/posts/cve-2019-10392.html  
https://misakikata.github.io/2019/09/CVE-2019-10392-Jenkins-2k19%E8%AE%A4%E8%AF%81%E8%BF%9C%E7%A8%8BRCE/
