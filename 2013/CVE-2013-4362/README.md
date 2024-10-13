# Automatic-davfs2-1.4.6-1.4.7-Local-Privilege-Escalation
Automatically exploit systems with vulnerable davfs2 (CVE-2013-4362)

## WHAT IS THIS FOR?
Just two .sh scripts to simplify the exploitation davfs2 with vulnerable versions

## Prerequisites 
* At least one of the module 'fuse' or 'coda' must not be loaded into the kernel (The PoC works with coda which is not loaded by default)
* You must be a user that is able to mount remote webdav servers
  * Check by `cat /etc/group | grep davfs2`
* davfs2 uses /etc/fstab to define which servers can be mounted by users. The user the attacker choses must be allowed to mount at least one remote webdav server
  * If authentication is needed, the attacker must be aware of the credentials
  * Check by `cat /etc/fstab | grep davfs`
  
## TO USE

1. Give executable permissions and run `auto_28806_kali.sh` on your kali machine
2. Follow the instructions and set up Python HTTP Server to serve the exploit files over to your victim
3. On your victim, download, give executable permissions and run `auto_28806_victim.sh`, it should download the needed exploit files
4. On your victim, use command `chmod +x /home/$user/rootprog`
5. On your victim, use command `chmod +x exploit.sh`
6. On your victim, run exploit with `./exploit.sh`, just press enter if the exploit asks you for anything
7. Hope ya get root!

## CREDITS
https://github.com/sectalks/sectalks/tree/master/ctf-solutions/SYD0x0b/z00nx
