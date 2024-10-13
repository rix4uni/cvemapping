# CVE-2020-16125-Reproduction
This repository is aimed at reproducing the attack . 

Description :
  Its original name is “Ubuntu gdm3 privilege escalation” , and it is found by a Github
security researcher named Kevin Backhouse . Its CVSS score is 4.6/10 (medium) and the
affected environment is Ubuntu version 20.04.1 with gdm3 version before 3.36.2 or 3.38.2 .
  The vulnerability is very easy to reproduce, and its influence is quite critical.

Analysis :
  The vulnerability is due to the unpredictable chain reaction between gdm3 and
Ubuntu due to their mechanism. Gdm3 with version before 3.36.2 or 3.38.2 would start
gnome-initial-setup if gdm3 can’t contact the accountservice via dbus in a timely manner
.Therefore, if the attacker can crash the accountservice, then the gnome-initial-setup will be
triggered ,and the attacker will be able to create a new privileged account (who has the
same privilege as root). Unfortunately, on Ubuntu with the early version, this can be done
by several simple steps since there’s a way to make accountsservice daemon process to
enter an infinite loop, which makes itself unresponsive. On the other hand, the vulnerability
is hard to be prevented, and it seems that the only way to prevent it is to update Ubuntu or
gdm3 to the new version.
