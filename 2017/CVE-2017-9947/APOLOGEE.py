#!/usr/bin/env python3

import requests
import xml.etree.ElementTree as ET
import socket
import struct
import sys

# Variables
device_ip = sys.argv[1]

# PXCM Web Server
url = f"http://{device_ip}/FieldPanel.xml"
response = requests.get(url)

# Download and Parse XML
xml_doc = response.content
root = ET.fromstring(xml_doc)

# Details
print("Remote Site ID:", root[18].text)
print("Building Level Network Name:", root[26].text)
print("Site Name:", root[27].text)
print("Hostname:", root[28].text)

# Big Endian
ip_addr = int(root[30].text, 16)
print("IP Address:", socket.inet_ntoa(struct.pack(">L", ip_addr)))

# Big Endian
gw_addr = int(root[32].text, 16)
gw_addr = str(socket.inet_ntoa(struct.pack(">L", gw_addr)))
print("Gateway IP Address:", gw_addr)

# Details
print("Ports:", root[49].text, root[50].text, root[51].text, root[52].text, root[53].text, root[54].text, root[55].text, root[56].text)
print("Maximum Transmission Size:", root[57].text)
print("BACnet Device Name:", root[60].text)
print("BACnet UDP Port:", root[62].text)
print("Device Location:", root[63].text)
print("Device Description:", root[64].text)

# Services
if int(root[48].text) == 1:
    print("Telnet Enabled")
else:
    print("Telnet Disabled")

if int(root[84].text) == 1:
    print("Wireless Enabled")
else:
    print("Wireless Disabled")

if int(root[103].text) == 3:
    print("Webserver Enabled")
else:
    print("Webserver Disabled")

# Details
print("Device Barcode:", root[88].text)
print("Device Revision String:", root[104].text)
print("Device Firmware:", root[105].text)
print("Panel Key Name:", root[109].text)
print("SNMP Username:", root[148].text)
print("SNMP Private Password:", root[149].text)
print("SNMP Authorization Password:", root[150].text)

