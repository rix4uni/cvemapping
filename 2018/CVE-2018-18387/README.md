# CVE-2018-18387
playSMS &lt; = 1.4.2 - Privilege escalation


TMHC TEAM found a vulnerability that lead to a priviledge escalation through playSMS/web/init.php that can lead to a complete system compromise.

The attacker need to get access on the box where playSMS is installed and be able to edit playSMS related files, and the daemon must be run as root. In the PHP code, references to a daemon were noticed. Research was conducted on the found daemon. The daemon was located in /usr/local/bin and it had associated files in /etc/init.d/.

This daemon is generally run by root, after being tested with a simple `whoami` command.

The daemon can't be directly modified, yet there is a `while` loop that runs every second which contains a `include init.php`. This file exists in `/var/www/html/playsms`.

Mitigations: Don't run the daemon as root.

The developers were contacted and a fix was released.

Playsms Contacts:

https://playsms.org 

https://github.com/antonraharja/playSMS
