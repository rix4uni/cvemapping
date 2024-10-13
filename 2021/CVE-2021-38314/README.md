# CVE-2021-38314 Python Exploit

## Detail
The Gutenberg Template Library & Redux Framework plugin <= 4.2.11 for WordPress registered several AJAX actions available to unauthenticated users in the `includes` function in `redux-core/class-redux-core.php` that were unique to a given site but deterministic and predictable given that they were based on an md5 hash of the site URL with a known salt value of '-redux' and an md5 hash of the previous hash with a known salt value of '-support'. These AJAX actions could be used to retrieve a list of active plugins and their versions, the site's PHP version, and an unsalted md5 hash of site's `AUTH_KEY` concatenated with the `SECURE_AUTH_KEY`. 

## Impact
Attacker can retrieve sensitive information such as a list of active plugins and their version, the site's PHP version, and an unsalted md5 hash of site's `AUTH_KEY` concatenated with the `SECURE_AUTH_KEY`.This would be most useful in causes where a separate plugin with an additional vulnerability was installed,as an attacker could use the information to save time and plan an intrusion.

## Exploit
Use:
    `python cve-2021-38314.py [ Vulnerable URL ]`

Example:
    `python cve-2021-38314.py https://example.com`

> Example PoC - https://youtu.be/n1e4aFmXvOk

## Links

[CVE-2021-38314](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-38314)

