# CUPS Honeypot

## Overview

This project implements a honeypot for capturing attempted exploitations of vulnerabilities in the CUPS (Common UNIX Printing System). Specifically, it is designed to monitor for exploitation attempts related to **CVE-2024-47177**. This vulnerability allows remote command execution through the `FoomaticRIPCommandLine` parameter in PPD files. If a malicious value is passed to this parameter, it can be executed as a user-controlled command, potentially leading to severe security breaches.

### CUPS and CVE-2024-47177

CUPS is a standards-based, open-source printing system used widely across various UNIX-like operating systems. The `cups-filters` package provides essential backends, filters, and utilities for CUPS 2.x on non-Mac OS systems. The critical flaw exploited in CVE-2024-47177 is the improper handling of the `FoomaticRIPCommandLine`, which can be leveraged in conjunction with other logic bugs, such as those described in **CVE-2024-47176**, to execute arbitrary commands on the host system.

This honeypot is designed to log exploit attempts by monitoring incoming print job requests and inspecting them for suspicious attributes, specifically focusing on the `printer-privacy-policy-uri` that may contain commands.

### Special Note

This project is inspired by the initial disclosure by [EvilSocket](https://www.evilsocket.net/2024/09/26/Attacking-UNIX-systems-via-CUPS-Part-I/), which highlights the security risks associated with CUPS and provides a comprehensive overview of the exploitation techniques involved.

## Features

- **Passive Monitoring**: The honeypot can run in a passive mode, listening for incoming print job requests without actively targeting a specific host.
- **Exploit Detection**: Captures and logs attempts to exploit the CUPS vulnerabilities by examining the attributes of print job requests.
- **Random Printer Configuration**: Automatically selects a random printer driver and generates a random printer name using available PPDs on the system.
- **UDP Packet Sending**: Optionally, it can send browsing packets to a specified target host, simulating a networked printer advertisement.

## Requirements

To run this honeypot, ensure you have the following dependencies installed:

- Ubuntu 23.x (tested)
- CUPS installed on your system
- The `cups` and `subprocess` Python libraries (included in standard Python installations)

## Installation

- Download and run the install.sh file:

   ```bash
   curl -sSL https://raw.githubusercontent.com/referefref/cupspot-2024-47177/refs/heads/main/install.sh | bash
   ```
## Usage

To run the honeypot, execute the following command:

```bash
python3 cupspot.py <LOCAL_HOST> [TARGET_HOST]
#<LOCAL_HOST>: The local address where the honeypot will listen for incoming print requests.
#[TARGET_HOST]: (Optional) The IP address of a target host to which browsing packets will be sent.
                #If omitted, the honeypot will run in passive mode.
```

## Example

Run the honeypot and send packets to a specific target:

```bash
python3 cupspot.py 127.0.0.1 192.168.1.100
```

Or run it in passive mode:

```bash
python3 cupspot.py 127.0.0.1
```





   
