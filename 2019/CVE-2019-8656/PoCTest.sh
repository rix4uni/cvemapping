#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Proper Usage POCTest.sh <IP Address Remote NFS Server>"
exit
fi

mkdir ~/Desktop/mnt
umount -t nfs $1:/nfs/Documents ~/Desktop/mnt
mount -t nfs $1:/nfs/Documents ~/Desktop/mnt
ls ~/Desktop/mnt/
