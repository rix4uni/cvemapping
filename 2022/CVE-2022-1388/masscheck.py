import threading
import requests
import argparse

requests.packages.urllib3.disable_warnings()


def usage():
    print(
        """
    +-----------------------------------------------------------------+
    Title: F5 BIG-IP iControl Rest API exposed Check                                   
    Usage Single URL：python check.py -u url
    Usage, List of URLS：python check.py -f url.txt
    Usage, Threaded python check.py -f url.txt -t
    +-----------------------------------------------------------------+                                     
    """
    )


def check(url):
    try:
        target_url = url + "/mgmt/shared/authn/login"
        res = requests.get(target_url, verify=False, timeout=3)
        if "resterrorresponse" in res.text:
            print(f"\033[0;31;22m[+] Host: {url} F5 iControl Rest API exposed \033[0m")
        else:
            print(f"\033[0;32;22m[-] Host: {url} F5 not vulnerable \033[0m")
    except Exception as e:
        print(f"\033[0;33;22m[x] Host: {url} Connection Fail \033[0m")


def run(filepath, threaded):
    urls = [x.strip() for x in open(filepath, "r").readlines()]
    if threaded:
        for u in urls:
            thread = threading.Thread(target=check, args=(u,))
            thread.start()
    else:
        for u in urls:
            check(u)
    return check


def main():
    parse = argparse.ArgumentParser()
    parse.add_argument("-u", "--url", help="Please check.py -u host")
    parse.add_argument("-f", "--file", help="Please check.py -f file")
    parse.add_argument(
        "-t",
        "--threaded",
        help="Please check.py -t threaded",
        action=argparse.BooleanOptionalAction,
        default=False,
    )
    args = parse.parse_args()
    url = args.url
    filepath = args.file
    threaded = args.threaded
    if url is not None and filepath is None:
        check(url)
    elif url is None and filepath is not None:
        run(filepath, threaded)
    else:
        usage()


if __name__ == "__main__":
    main()
