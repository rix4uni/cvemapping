from scapy.all import *
 
bt = BluetoothL2CAPSocket("01:02:03:04:05:06")
 
bt.recv()
