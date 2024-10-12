# CVE-2023-33105: Transient DOS in WLAN Host and Firmware

## Overview

This repository contains the exploit code for CVE-2023-33105, a vulnerability identified in Qualcomm devices. The exploit leverages authentication frames to perform a denial of service (DoS) attack on a target access point (AP) by sending a large number of open authentication frames with an invalid transaction sequence number.

- **CVE ID**: [CVE-2023-33105](https://nvd.nist.gov/vuln/detail/CVE-2023-33105)
- **Qualcomm Security Bulletin**: [March 2024 Bulletin](https://docs.qualcomm.com/product/publicresources/securitybulletin/march-2024-bulletin.html)

## Requirements

- Python 3.x
- Scapy
- Termcolor
- Airodump-ng
- A wireless network adapter capable of injection

## Installation

To install the necessary Python libraries, run:

```bash
pip install -r requirements.txt
```

## Files

- `config.py`: Configuration file for setting target MAC addresses and parameters.
- `exploit_v2.py`: Main exploit script.

## Configuration

Before running the exploit, update the `config.py` file with the target MAC addresses and other parameters.

```python
# config.py

# MAC address of the station (client)
sta_target = 'XX:XX:XX:XX:XX:XX'  # change this

# MAC address of the access point (AP)
ap_target = 'YY:YY:YY:YY:YY:YY'  # change this

# Number of frames to send
spray = 500

# Interval for checking if the BSSID is still up (in seconds)
check_interval = 60
```

## Usage

To run the exploit, follow these steps:

1. Ensure your wireless network adapter is in monitor mode. You can enable monitor mode using the following command:

```bash
sudo ip link set wlan0 down
sudo iw dev wlan0 set type monitor
sudo ip link set wlan0 up
```

2. Execute the exploit script:

```bash
python exploit_v2.py
```

The script will send a large number of open authentication frames with invalid transaction sequence numbers to the target AP, causing a transient DoS.

## FAQ

### What is CVE-2023-33105?

CVE-2023-33105 is a vulnerability in Qualcomm devices that allows a transient DoS in WLAN Host and Firmware when a large number of open authentication frames are sent with an invalid transaction sequence number.

### What are the requirements to run this exploit?

You need Python 3.x, Scapy, Airodump-ng, and a wireless network adapter capable of injection.

### Is it legal to use this exploit?

Unauthorized use of this script against networks without permission is illegal. This code is provided for educational purposes only.

## References

- [CVE-2023-33105](https://nvd.nist.gov/vuln/detail/CVE-2023-33105)
- [Qualcomm Security Bulletin](https://docs.qualcomm.com/product/publicresources/securitybulletin/march-2024-bulletin.html)
