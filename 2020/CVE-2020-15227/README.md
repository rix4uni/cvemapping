# CVE-2020-15227

DISCLAIMER! I take no responsibility of using it in wild life environment so please do NOT do it. This thingy is just to demonstrate and for test things for sysadmins

---

This tool tests for [vulnerability](https://github.com/nette/application/security/advisories/GHSA-8gv3-3j7f-wg94) in [nette/application](https://github.com/nette/application).

# How to fix the vulnerability

## Composer

Update dependency to the latest version.

* ``nette/application >=3.0.6``
* ``nette/application >=2.4.16``
* ``nette/application >=2.3.14``
* ``nette/application >=2.2.10``
* ``nette/nette >= 2.1.13``
* ``nette/nette >= 2.0.19``

Add a new dependency [``roave/security-advisories``](https://github.com/Roave/SecurityAdvisories) into the project

## Third-party patch tools

* [PHP tool by @dg](https://gist.github.com/dg/be0f26b31be15a2f1b1208a1714bf415)
* [Bash tool by @spaze](https://gist.github.com/spaze/fb6d8cdc296e0314b50f8b484bcd1385)

# Description

**List of tested vulnerabilities:**

- file_put_contents
- Nette\\Utils\\FileSystem::write
- shell_exec

# Requiments

* Python 3.x

# Usage

```bash
git clone https://github.com/filipsedivy/CVE-2020-15227
cd CVE-2020-15227
python main.py https://example.com
```

OR

```
wget https://github.com/filipsedivy/CVE-2020-15227/archive/master.zip
unzip master.zip
cd CVE-2020-15227-master
python main.py https://example.com
```

[![asciicast](https://asciinema.org/a/373111.svg)](https://asciinema.org/a/373111)

# API

## Example

```python
from CVE_2020_1522 import CVE_2020_15227

# Disable verbose
cve = CVE_2020_15227(verbose=False)

# Response True or False
result = cve.run("https://example.com")

if result is True:
    print('Fuck! Confirmed vulnerability! :-( Need update composer')
else:
    print('Good night! Everything is okay. :)')

```

# Related links
* [cve.mitre.org - CVE-2020-15227](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-15227)
* [blog.nette.org - CVE-2020–15227: Potential Remote Code Execution Vulnerability](https://blog.nette.org/en/cve-2020-15227-potential-remote-code-execution-vulnerability)
* [michalspacek.com - Don't let security bugs catch you off guard](https://www.michalspacek.com/dont-let-security-bugs-catch-you-off-guard)
* [blog.nette.org - CVE-2020–15227: Chyba potenciálně umožňující vzdálené spuštění kódu](https://blog.nette.org/cs/cve-2020-15227-chyba-potencialne-umoznujici-vzdalene-spusteni-kodu)
* [michalspacek.com - Ať vás bezpečnostní chyby nenachytají na švestkách](https://www.michalspacek.cz/at-vas-bezpecnostni-chyby-nenachytaji-na-svestkach)
* [phpfashion.com - Objevena první zranitelnost v Nette, aktualizujte!](https://phpfashion.com/objevena-prvni-zranitelnost-v-nette-aktualizujte)