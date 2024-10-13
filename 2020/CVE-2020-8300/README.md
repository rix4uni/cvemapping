
Detect Citrix ADC SAML action or SAML iDP Profile config vulnerable to CVE-2020-8300 using Citrix ADC NITRO API

![image](https://user-images.githubusercontent.com/8889050/122010412-03b58580-cdb3-11eb-9708-9a027d871070.png)


EXAMPLE
& '.\CitrixADC-CVE-2020-8300.ps1' -NSIPProtocol http -NSIP 10.10.10.10 -user nitro -pass "SshhhItsASecret"


If this proves useful to anyone I will develop further with the following functionality:

- Identify bindings for SAML Actions and SAML iDP Profiles to identify if and where they are in use
- Detect vulnerable firmware versions by seeing if the relaystaterule and acsurlrule parameters can be set 
