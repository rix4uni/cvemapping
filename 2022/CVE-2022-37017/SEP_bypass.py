import os, ctypes
as_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
base = "C:\\Program Files (x86)\\Symantec\\\Symantec Endpoint Protection\\"
version = os.listdir(base)[0]
wd = base + version + "\\Bin\\"
with open(wd + "SymCorpUI.exe", 'rb') as fp:
    f = fp.read()
f = f.replace(b'\x74\x0a\x8b\xce\xff\x15', b'\x75\x0a\x8b\xce\xff\x15')
"""
f.find(b'\x74\x0a\x8b\xce\xff\x15') - >
78196     14.0.3872.1100
110883    14.3.558.0000
226371    14.3.5413.3000
"""
patched = './SymCorpUI_patched.exe'
compat = "" if as_admin else "set __COMPAT_LAYER=RUNASINVOKER && " 
with open(patched, 'wb') as fp:
    fp.write(f)
os.system(compat + 'start /D "' + wd + '" ' + patched )
