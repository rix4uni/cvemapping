#!/bin/bash

#create a publicily accessible NFS share and put the .app in it

mkdir -p /nfs/Documents
echo '/nfs/Documents *(insecure,rw,no_root_squash,anonuid=1000,anongid=1000,async,nohide)' >> /etc/exports
apt update
apt install nfs-kernel-server
service nfs-kernel-server restart
echo "IP Address"
hostname -I
