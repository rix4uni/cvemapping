import base64
import re

import requests


def getToken(host, username, password):
    resp = requests.post(
        f"https://{host}/cgi-bin/authLogin.cgi",
        verify=False,
        data = {
            'user': username,
            'serviceKey': 1,
            'client_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.159 Safari/537.36',
            'client_app': 'Web Desktop',
            'pwd': base64.b64encode(password.encode('ascii')),
            'client_id': '3eafe415-4986-4baa-b13c-0eefc4c5f9f6',
            'r': '0.8916667046237661'
        }
    )
    resp.raise_for_status()
    authSidRE = "<authSid><!\\[CDATA\\[(.{8})\\]\\]></authSid>"
    matches = list(re.finditer(authSidRE.encode('ascii'), resp.content))
    if len(matches) == 0:
        raise Exception("Login failed")
    sid =matches[0].groups()[0].decode('ascii')

    return sid


def parseArgs(parser):
    return parser.parse_args()
