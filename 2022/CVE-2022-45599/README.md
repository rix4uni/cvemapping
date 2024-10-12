# CVE-2022-45599

| CVE URL:           | https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-45599 |
|--------------------|---------------------------------------------------------------|
| Reported by:       | TanYeeTat                                                     |
| Product:           | Aztech WMB250AC Wireless Mesh Routers                         |
| Affected Firmware: | 2020 Release (``topaz-linux.lzma.img``)              |
| Firmware download: | closed source                                                 |


![aztech-wmb250ac](./sshots/aztech-wmb250ac.png)

![product-aztech-kylaconnect-site](./sshots/product-aztech-kylaconnect-site.png)
> Product Manual: https://kylaconnect.com/download-center/

> Vulnerability was reported to Aztech's security team via security@aztech.com on **7th June 2022**, with no response as of 21st February 2023
> - [Kylaconnect Vulnerability Disclosure](https://kylaconnect.com/vulnerability-disclosure-policy/)


## Vulnerability Details

A PHP Type Juggling vulnerability exists in the ``login.php`` web page on port ``80``, in the ``password`` authentication field, that allows an attacker to authenticate without knowledge of the admin's password. This however, has a very low probability of occurance, as the admin's MD5-hashed password has start with a ``0e`` and followed by **numbers**. A comprehensive list of plaintext passwords and their corresponding MD5 hashes that are succeptible to a PHP Type Juggling Attack is provided below, along with a reference blog that explains it in detail.

> [MD5 Type Juggling List](https://github.com/spaze/hashes/blob/master/md5.md)
>
> [Whitehatsec Blog Magic Hashes](https://www.whitehatsec.com/blog/magic-hashes/)


**TLDR**: The PHP source code in ``login.php`` that handles the authentication checks are performed with Loose Comparison (``==``, two equal signs), instead of using a Strict Comparison (``===``, three equal signs).

![login-php-loose-comparison](./sshots/login-php-loose-comparison.png)


## Proof Of Concept

1. Configure the admin user's password to be a plaintext value that when MD5-hashed results in it starting with a ``0e`` and followed by numbers
	- e.g., Plaintext: ``PJNPDWY``, MD5: ``0e291529052894702774557631701704``
	> ![modified-admin-conf](./sshots/modified-admin-conf.png) 
	>
	> Note: an invalid hash of ``0e123456789012345678901234567890`` will work as well
	
2. Authenticate as the admin user on the web service with username ``admin`` and any plaintext password found in [MD5 Type Juggling List](https://github.com/spaze/hashes/blob/master/md5.md) (e.g., ``240610708``)
