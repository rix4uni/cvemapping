import requests
import json

survey_url = input("Enter the survey URL. It should look like this https://example.com/s/NHi3uoeKOkZdwaCU7Dea : ")

api_url = survey_url.replace("/s/", "/api/ngsurveys/")
r_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0", "Accept": "application/json, text/plain, */*", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Connection": "close"}
request = requests.get(api_url, headers=r_headers)

print(request.status_code)

json_response = request.json()

for key, value in json_response.items():
	if key == "survey":
		password = value["accessPassword"]

if password:
	print("The password is " + password)
else:
	print("The password could not be retrieved. Possibly because there's no password set for this survey.")

