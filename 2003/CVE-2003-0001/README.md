# Etherleak Vulnerability Checker

This Python script helps to detect the Etherleak (CVE-2003-0001) vulnerability on a target host by analyzing the padding data in network packets. The script uses Scapy to send various types of requests (ICMP, ARP, or TCP) and checks if the responses contain any padding data that could potentially leak sensitive memory contents.

## Etherleak Overview
Etherleak is a vulnerability where network drivers improperly pad Ethernet frames with leftover memory. Attackers can exploit this by sending certain requests (ICMP, ARP, or TCP) and analyzing the response packets to see if they leak sensitive data from system memory.
### Prerequisites
- Python 3.x or higher
- Scapy: You can install Scapy using pip:
```bash
    pip install scapy
```

## Usage
The script supports three protocols for probing the target: ARP, ICMP, or TCP. 
If using TCP, you can specify a port, with the default being 445 (commonly used by SMB).

Command Line Usage
```bash
sudo python etherleak_checker.py <target_ip> <arp|icmp|tcp> <count> [tcp_port]

    <target_ip>: The IP address of the target host.
    <arp|icmp|tcp>: The type of request to send (ARP, ICMP, or TCP).
    <count>: The number of packets to send and analyze.
    [tcp_port]: (Optional) The TCP port to target if using tcp (default: 445).
```

### Examples

#### ICMP (Ping) Test:

```bash

sudo python etherleak_checker.py 192.168.1.1 icmp 10
```
This will send 10 ICMP echo requests (pings) to the target IP 192.168.1.1 and analyze the padding data in the responses.

#### ARP Test:

```bash

sudo python etherleak_checker.py 192.168.1.1 arp 10
```
This will send 10 ARP requests to the target IP 192.168.1.1 and analyze the padding data in the ARP responses.

#### TCP Test on Default Port 445:

```bash

sudo python etherleak_checker.py 192.168.1.1 tcp 10
```
This will send 10 TCP SYN packets to the target IP 192.168.1.1 on port 445 (SMB) and analyze the padding data in the TCP responses.

#### TCP Test on Custom Port (e.g., Port 80):

```bash

    sudo python etherleak_checker.py 192.168.1.1 tcp 10 80
```
This will send 10 TCP SYN packets to port 80 of the target IP 192.168.1.1 and analyze the padding data in the responses.

### How It Works

- Packet Sending: The script sends ICMP, ARP, or TCP requests to the target. If TCP is selected, you can specify the port.
- Response Capturing: The script listens for responses and checks if they contain a Padding layer.
- Padding Analysis: The captured padding is compared across multiple packets. If variation in padding is detected, the host is potentially vulnerable to Etherleak.
- Output: A clear message will inform you if the host is likely vulnerable based on the variation in the padding.

### Output Example
```
[ Targeting 192.168.1.1 using ICMP for 10 requests... ]
Padding captured: 00 00 00 01 02 03 ...
Padding captured: 00 00 00 01 02 03 ...
...
Variation in padding data detected across packets, indicating a potential Etherleak vulnerability.

Padding analysis complete.
```

### Disclaimer
This script is intended for educational purposes and for testing your own systems in a controlled environment. Unauthorized use of this script against systems without permission is illegal and unethical. Always ensure you have proper authorization before running tests against any system.
