#!/bin/sh

set -euo pipefail

ORIGINAL_FILE=/usr/local/modules/cgi/nas_sharing.cgi
PATCHED_FILE=/usr/local/config/nas_sharing_patched.cgi
TWO_NOPS='\x00\xf0\x20\xe3\x00\xf0\x20\xe3'
SYSTEM_CALL_OFFSET=29984

# Grab a copy of the vulnerable bin and put it somewhere we can modify it
cp $ORIGINAL_FILE $PATCHED_FILE

# Where the magic happens
printf $TWO_NOPS | dd of=$PATCHED_FILE bs=1 seek=$SYSTEM_CALL_OFFSET count=8 conv=notrunc

# Update the symlink to our fixed version
ln -fs $PATCHED_FILE /var/www/cgi-bin/nas_sharing.cgi

echo "Done"