import socket

host = "localhost"
port = 80                   # The same port as used by the server
buf = b'A'*10000

try:
    for i in range(50):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.sendall(buf)
        data = s.recv(1024)
        s.close()
        print('Received', repr(data))
except:
    print("Completed...")
