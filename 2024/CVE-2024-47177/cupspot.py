#!/usr/bin/python3

import cups
import subprocess
import random
import string
import socket
import threading
import time
import sys
import logging

from http.server import BaseHTTPRequestHandler, HTTPServer

logging.basicConfig(filename='honeypot_exploit.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def get_available_ppds():
    """Run lpinfo -m to get available PPDs and return as a list."""
    try:
        result = subprocess.run(['lpinfo', '-m'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        ppds = result.stdout.splitlines()
        if not ppds:
            raise Exception("No PPDs found on the system.")
        return ppds
    except subprocess.CalledProcessError as e:
        print(f"Error running lpinfo -m: {e}")
        return []

def choose_random_ppd(ppds):
    """Select a random PPD from the available list."""
    return random.choice(ppds).split(' ')[0]

def generate_random_printer_name(length=8):
    """Generate a random printer name with letters and digits."""
    return 'Printer_' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def detect_exploit(printer_attributes):
    """Detect potential exploit attempts by looking for command injection in printer-privacy-policy-uri."""
    if b'printer-privacy-policy-uri' in printer_attributes:
        policy_value = printer_attributes[b'printer-privacy-policy-uri']
        if b'FoomaticRIPCommandLine' in policy_value:
            logging.info(f"Exploit attempt detected: {policy_value}")
            print(f"[ALERT] Exploit attempt detected: {policy_value}")
            return True
    return False

def handle_print_request(request_data):
    """Handle print job requests and check for exploits."""
    print("Received print job, parsing attributes...")

    if detect_exploit(request_data):
        print("Exploit attempt captured!")
    else:
        print("No exploit detected in this request.")

def start_fake_printer_listener(server_host, server_port):
    """Fake printer server to listen for connections and inspect requests."""
    server_address = (server_host, server_port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f"Fake printer server listening on {server_host}:{server_port}")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()
        print(f"Shutting down fake printer server on {server_host}:{server_port}")

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    """HTTP handler to simulate printer server and capture request data."""
    def do_POST(self):
        length = int(self.headers['Content-Length'])
        request_data = self.rfile.read(length)

        print(f"Received a print job from {self.client_address[0]}")

        handle_print_request(request_data)
        self.send_response(200)
        self.end_headers()

def run_cups_fake_printer():
    ppds = get_available_ppds()
    if not ppds:
        print("No PPDs found. Please install PPDs or printer drivers.")
        return

    random_ppd = choose_random_ppd(ppds)
    random_printer_name = generate_random_printer_name()

    print(f"Selected PPD: {random_ppd}")
    print(f"Generated Printer Name: {random_printer_name}")

    conn = cups.Connection()
    try:
        conn.addPrinter(random_printer_name, ppdname=random_ppd, device='file:/dev/null')
        conn.enablePrinter(random_printer_name)
        conn.acceptJobs(random_printer_name)
        print(f"Printer {random_printer_name} added successfully.")
    except cups.IPPError as e:
        print(f"Failed to add printer: {e}")

def send_browsed_packet(ip, port, ipp_server_host, ipp_server_port):
    """Send a UDP packet to advertise the printer to the target host."""
    print("Sending UDP packet to %s:%d ..." % (ip, port))

    printer_uri = 'http://%s:%d/printers/%s' % (ipp_server_host, ipp_server_port, generate_random_printer_name())

    message = bytes(f'0 3 "{printer_uri}" "Office HQ" "Printer"', 'UTF-8')

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message, (ip, port))

def wait_until_ctrl_c():
    try:
        while True:
            time.sleep(300)
    except KeyboardInterrupt:
        return

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print(f"Usage: {sys.argv[0]} <LOCAL_HOST> [TARGET_HOST]")
        quit()
    run_cups_fake_printer()

    SERVER_HOST = sys.argv[1]
    SERVER_PORT = 12345

    threading.Thread(target=start_fake_printer_listener, args=(SERVER_HOST, SERVER_PORT)).start()
    if len(sys.argv) == 3:
        TARGET_HOST = sys.argv[2]
        send_browsed_packet(TARGET_HOST, 631, SERVER_HOST, SERVER_PORT)

    print("Waiting for incoming connections and potential exploit attempts...")
    wait_until_ctrl_c()
