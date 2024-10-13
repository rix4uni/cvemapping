## American Unsigned Language
#### by zx2c4

These are two exploits to disable kernel lockdown via ACPI table injection.

`american-unsigned-language.sh` is for Ubuntu 18.04 Bionic's 4.15 kernel with their custom patches and uses one technique. [CVE-2019-20908](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2019-20908).

`american-unsigned-language-2.sh` is for mainline/upstream kernels and uses a different technique. [CVE-2020-15780](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-15780).

Explanation is in the headers of each script.

![Demo](https://git.zx2c4.com/american-unsigned-language/blob/demo.gif)
