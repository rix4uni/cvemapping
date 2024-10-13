#!/usr/bin/python3
import random
import hexdump
import string
import socket
import struct
from sys import argv, exit


def ike_cipher(t_id, keylen=0):
    ret = [t_id, 0]

def random_string(size):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))

def create_nonce(nxt, nonce):
    ret = bytearray()
    ret.append(nxt)
    ret.append(0)
    ret.append(0)       # len hi
    ret.append(0)       # len lo
    for i in nonce:
        ret.append(ord(i))
    ret[2] = (len(ret) & 0xff00) >> 8
    ret[3] = len(ret) & 0xff
    return ret




def create_ke(nxt, group, data):
    ret = bytearray()
    ret.append(nxt)
    ret.append(0)       # reserved
    ret.append(0)       # len hi
    ret.append(0)       # len lo
    ret.append((group & 0xff00) >> 8)
    ret.append(group & 0xff)
    ret.append(0)
    ret.append(0)
    for i in data:
        ret.append(ord(i))
    ret[2] = (len(ret) & 0xff00) >> 8
    ret[3] = len(ret) & 0xff
    return ret

def create_vendorid(vid):
    ret = bytearray()
    ret.append(0)       # reserved
    ret.append(0)       # reserved
    ret.append(0)       # len hi
    ret.append(0)       # len lo
    for i in vid:
        ret.append(i)
    ret[2] = (len(ret) & 0xff00) >> 8
    ret[3] = len(ret) & 0xff
    return ret


def create_proposal(transforms, integrities, groups, prfs, nxt, num):
    tlist = []
    attr = None
    ret = bytearray()
    for i in transforms:
        t_id = i[0]
        klen = i[1]
        if klen > 0:
            attr = create_trans_attr(14, klen)
        else:
            attr = None
        tlist.append(create_transform(3, 1, t_id, attr))
    for i in integrities:
        tlist.append(create_transform(3, 3, i, None))
    for i in groups:
        tlist.append(create_transform(3, 4, i, None))
    for i in prfs:
        tlist.append(create_transform(3, 2, i, None))

    tlist[-1][0] = 0    
    ret.append(nxt)             # next payload
    ret.append(0)               # reserved
    ret.append(0)               # len hi
    ret.append(0)               # len lo
    ret.append(num)
    ret.append(1)
    ret.append(0)
    ret.append(len(tlist))
    for i in tlist:
        for j in i:
            ret.append(j)
    ret[2] = (len(ret) & 0xff00) >> 8
    ret[3] = len(ret) & 0xff
    return ret
    


def create_transform(t_next,t_type, t_id, t_attribs):
    ret = bytearray()
    ret.append(t_next)      # next
    ret.append(0)           # reserved
    ret.append(0)           # len hi
    ret.append(0)           # len lo
    ret.append(t_type)
    ret.append(0)           # reserved
    ret.append((t_id & 0xff00) >> 8)
    ret.append(t_id & 0xff)
    if not t_attribs is None:
        for a in t_attribs:
            ret.append(a)
    ret[2] = (len(ret) & 0xff00) >> 8
    ret[3] = (len(ret) & 0xff)
    return ret

            
def create_sa(nxt, proposal):
    ret = bytearray()
    ret.append(nxt)
    ret.append(0)
    ret.append(0)           # len hi
    ret.append(0)           # len lo
    for i in proposal:
        ret.append(i)
    ret[2] = (len(ret) & 0xff00) >> 8
    ret[3] = len(ret) & 0xff
    return ret


def create_trans_attr(attr_type, attr_val):
    ret = bytearray()
    top = 0x8000 + attr_type
    ret.append((top & 0xff00) >> 8)
    ret.append(top & 0xff)
    ret.append((attr_val & 0xff00) >> 8)
    ret.append(attr_val & 0xff)
    return ret

def create_isakmp(ispi, xchg, first, sa, ke, nonce, vid):
    ret = bytearray()
    for i in ispi:
        ret.append(i)           # init SPI
    for i in range(8):
        ret.append(0)           # resp SPI
    ret.append(first)
    ret.append(0x20)
    ret.append(xchg)
    ret.append(0x08)
    ret.append(0)               # message id
    ret.append(0)               # message id
    ret.append(0)               # message id
    ret.append(0)               # message id
    ret.append(0)               # len 
    ret.append(0)               # len 
    ret.append(0)               # len 
    ret.append(0)               # len 
    
    for i in sa:
        ret.append(i)
    for i in ke:
        ret.append(i)
    for i in nonce:
        ret.append(i)
    for i in vid:
        ret.append(i)
    l = len(ret)
    ret[24] = (l & 0xff000000) >> 24
    ret[25] = (l & 0xff0000) >> 16
    ret[26] = (l & 0xff00) >> 8
    ret[27] = l & 0xff
    return ret


def bytearray_sum(data):
    l = len(data)
    shift = l*8
    ret = 0
    while l >= 0:
        ret = ret + (data[l] << shift)
        shift = shift - 8
        l = l - 1

def parse_sa(sa):
    ret = dict()
    ret['next_payload'] = sa[0]
    ret['length'] = bytearray_sum(sa[2:3])
    return ret


def parse_isakmp(isakmp):
    ret = dict()
    ret['init_spi'] = isakmp[0:7]
    ret['resp_spi'] = isakmp[8:15]
    ret['next_payload'] = isakmp[16]
    ret['version'] = isakmp[17]
    ret['exchange_type'] = isakmp[18]
    ret['flags'] = isakmp[19]
    ret['msg_id'] = isakmp[20:23]
    ret['len'] = bytearray_sum(isakmp[24:25])
    if ret['next_payload'] == 33:
        ret['sa'] = parse_sa(isakmp[26:-1])
    return ret


def create_frag_isakmp(irpi, rspi, nxt,  xchg_type, flags, msg_id, frag_id, frag_seq, frag_last, data = None):
    ret = bytearray()
    for i in ispi:
        ret.append(i)
    for i in rspi:
        ret.append(i)
    ret.append(nxt)
    ret.append(0x20)
    ret.append(xchg_type)
    ret.append(flags)
    for i in msg_id:
        ret.append(i)
    ret.append(0)           # len
    ret.append(0)
    ret.append(0)
    ret.append(0)           # end len
    for i in frag(frag_id, frag_seq, frag_last, data=data, ispi=ispi, rspi=rspi, msg_id=msg_id):
        ret.append(i)
    l = len(ret)
    ret[24] = (l & 0xff000000) >> 24
    ret[25] = (l & 0xff0000) >> 16
    ret[26] = (l & 0xff00) >> 8
    ret[27] = l & 0xff
    return ret


def create_e_and_a(ispi, rspi, msg_id, data):
    ret = bytearray()
    for i in ispi:
        ret.append(i)
    for i in rspi:
        ret.append(i)
    ret.append(46)      # encrypted and authenticated
    ret.append(0x20)
    ret.append(34)
    ret.append(0x08)
    for i in msg_id:
        ret.append(i)
    ret.append(0)       # len
    ret.append(0)       # len
    ret.append(0)       # len
    ret.append(0)       # len
    ret.append(0)       # E&A next
    ret.append(0)       # E&A critical
    ret.append(0)       # E&A len
    ret.append(0)       # E&A len
    for i in data:
        ret.append(ord(i))
    ret[30] = ((len(data)+4) & 0xff00) >> 8
    ret[31] = (len(data)+4) & 0xff
    l = len(ret)
    ret[24] = (l & 0xff000000) >> 24
    ret[25] = (l & 0xff0000) >> 16
    ret[26] = (l & 0xff00) >> 8
    ret[27] = l & 0xff
    return ret


        

def frag(frag_id, frag_seq, frag_last, data = None, ispi = None, rspi = None, msg_id = None):
    ret = bytearray()
    ret.append(0)
    ret.append(0)
    ret.append(0)           # payload len
    ret.append(0)           # payload len
    for i in frag_id:
        ret.append(i)
    ret.append(frag_seq)
    ret.append(frag_last)
    if not data is None:
        for i in create_e_and_a(ispi, rspi, msg_id, data):
            ret.append(i)
    ret[2] = (len(ret) & 0xff00) >> 8
    ret[3] = len(ret) & 0xff
    return ret
    
     
def print_notify(notify_payload):
    print("\tNext payload: ", end="")
    if int(notify_payload[0]) == 0:
        print("NONE")
    else:
        print(notify_payload[0])
    print("\tCritical bit ", end="")
    if int(notify_payload[1]) == 0:
        print("Not Critical")
    else:
        print("Critical")
    plen = struct.unpack("!h", notify_payload[2:4])[0]
    print("\tPayload length: %d" % plen)
    print("\tProtocol ID: ", end="")
    if notify_payload[4] == 1:
        print("IKE")
    print("\tSPI Size: %d" % int(notify_payload[5]))
    print("\tNotify Message Type: ", end="")
    if  struct.unpack("!h", notify_payload[6:8])[0] == 7:
        print("Invalid Syntax")
    else:
        print("unknown")
        print("[-] Not vulnerable... exiting.")
        exit(1)
    print("\tNotification DATA: ", end="")
    if  plen > 8:
        print(notify_payload[8])
        print("[-] Not vulnerable... exiting.")
    else:
        print("missing")
        print("[+] Notification data is missing. ASA is vulnerable.")


if len(argv) < 2 or not argv[1].__contains__(":"):
    print("usage: %s ip:port" % argv[0])
    exit(1)

    
ip = argv[1].split(":")[0]
port = int(argv[1].split(":")[1])

print("""This tool is used to verify the presence of CVE-2016-1287, an unauthenticated remote code execution vulnerability affecting Cisco's ASA products.
No attempt will be made to execute code, this simply observes behavior of affected versions when malformed fragments are sent to the ASA.
Continue? [y/N] """)
if not input().lower() == "y":
    exit(1)
    


transforms = [
                [2, 0],
                [3, 0],
                [11, 0],
                [12, 0],
                [12, 192],
                [12, 256],
                [20, 0],
                [20, 192],
                [20, 256],
             ]

integrity = [1, 2, 12, 13, 14]
groups = [1, 2, 5, 14, 19, 20, 21, 24]
prf = [1, 2, 5, 6, 7]

prop = create_proposal(transforms, integrity, groups, prf, 0, 1)
sa = create_sa(34, prop)

cisco_vid = [ 0x40, 0x48, 0xb7, 0xd5, 0x6e, 0xbc, 0xe8, 0x85, 0x25, 0xe7, 0xde, 0x7f, 0x00, 0xd6, 0xc2, 0xd3 ]


nonce = create_nonce(43, random_string(32))
vid = create_vendorid(cisco_vid)

ke_group = 2
ispi = random_string(8)
ispi = bytearray()
ispi.append(0x66)
ispi.append(0x53)
ispi.append(0x54)
ispi.append(0x71)
ispi.append(0x45)
ispi.append(0x49)
ispi.append(0x58)
ispi.append(0x64)



sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
for i in range(3):
    if ke_group == 1:
        dhlen = 96
    elif ke_group == 2:
        dhlen = 128
    elif ke_group == 5:
        dhlen = 192
    elif ke_group == 14: 
        dhlen = 256
    elif ke_group == 19: 
        dhlen = 64; 
    elif ke_group == 20: 
        dhlen = 96 
    elif ke_group == 21:
        dhlen = 132
    else:
        dhlen = 256

    dhpub = random_string(dhlen)
    ke = create_ke(40, ke_group, dhpub)

    isakmp = create_isakmp(ispi, 34, 33, sa, ke, nonce, vid)


    print("[*] Sending Initiator Request")
    sock.sendto(isakmp, (ip, port))

    resp, _ =  sock.recvfrom(2048)

    print("[*] Received Response")
    
            
    # Valid SA
    if resp[16] == 33:
        print("[+] Valid SA found. Moving on")
        break
    print("[-] Invalid SA. Trying another...")

cisco = 0
c_frag = 0

#parsed_resp = parse_isakmp(resp)
resp_spi = resp[8:16]
msg_id = bytearray()
msg_id.append(0)
msg_id.append(0)
msg_id.append(0)
msg_id.append(1)



first_frag = create_frag_isakmp(ispi, resp_spi, 132, 35, 0x08, msg_id, [0,1], 1, 0 )

second_frag = create_frag_isakmp(ispi, resp_spi, 132, 35, 0x08, msg_id, [0,1], 2, 1, "BAADBAADBAADBAAD")

print("[*] Sending first fragment")
sock.sendto(first_frag, (ip, port))
print("[*] Sending second fragment")
sock.sendto(second_frag, (ip, port))

timeout = False

sock.settimeout(5.0)
try:
    resp, _ =  sock.recvfrom(2048)
except socket.timeout:
    print("[*] IKE Fragment was dropped indicating the ASA is not vulnerable.")
    timeout = True
    exit(1)
#Check for notify payload
if resp[16] == 41:
    print("[*] Notify Payload found. Printing Notify payload data.")
    print_notify(resp[28:])
    hexdump.hexdump(resp)
