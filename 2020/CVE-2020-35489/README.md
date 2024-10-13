# Check-WP-CVE-2020-35489

## CVE-2020-35489
The CVE-2020-35489 is discovered in the WordPress plugin Contact Form 7 5.3.1 and older versions. By exploiting this vulnerability, attackers could simply upload files of any type, bypassing all restrictions placed regarding the allowed upload-able file types on a website.

An estimated **5 million** websites were affected.

The PoC will be displayed on December 31, 2020, to give users the time to update.

## Reference
https://wpscan.com/vulnerability/10508

https://contactform7.com/2020/12/17/contact-form-7-532/#more-38314

https://cwe.mitre.org/data/definitions/434.html

## Run script
```
$ python3 check_CVE-2020-35489.py -d domaintest.com

Contact Form 7 version: 5.1.3
domaintest.com is vulnerable!
```

```
$ python3 check_CVE-2020-35489.py -i in.txt -o out.txt
```