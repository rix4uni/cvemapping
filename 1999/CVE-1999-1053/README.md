# CVE-1999-1053 Proof-of-Concept Exploit

## Background

This Proof-of-Concept(PoC) exploit is inspired from a CTF web challenge called `CVE 1999` in HKCERT CTF 2022. (Writeup [link](https://siunam321.github.io/ctf/HKCERT-CTF-2022/Web/CVE-1999/))

## Information

**Description:** In Matt Wright Guestbook <= 2.3.1, there is a Server-Side Include injection vulnerability that allows unauthenticated user to execute arbitrary code.
**Original author:** Patrick
**Original Exploit-DB link:** https://www.exploit-db.com/exploits/9907

## Proof-of-Concept Exploit

### Description

> The Matt Wright `guestbook.pl` <= v2.3.1 CGI script contains a flaw that may allow arbitrary command execution. The vulnerability requires that HTML posting is enabled in the `guestbook.pl` script, and that the web server must have the Server-Side Include (SSI) script handler enabled for the '`.html`' file type. By combining the script weakness with non-default server configuration, it is possible to exploit this vulnerability successfully. (From [Exploit-DB](https://www.exploit-db.com/exploits/9907))

### Installation

```bash
wget https://raw.githubusercontent.com/siunam321/CVE-1999-1053-PoC/main/CVE-1999-1053-PoC.py
```

### Usage/Exploitation

- `-u` or `--url` to supply the target full URL
- `-p` or `--payload` to supply the payload

### Screenshot

![](https://github.com/siunam321/CVE-1999-1053-PoC/blob/main/images/poc1.png)

![](https://github.com/siunam321/CVE-1999-1053-PoC/blob/main/images/poc2.png)

![](https://github.com/siunam321/CVE-1999-1053-PoC/blob/main/images/poc3.png)