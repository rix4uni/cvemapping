# GL.iNet Router Authentication Bypass (CVE-2023-46453) Exploit

This repository contains an exploit script for CVE-2023-46453, a remote authentication bypass vulnerability found in the web interface of GL.iNet routers running firmware versions 4.x and up. By exploiting this vulnerability, an attacker can gain unauthorized access to the router's web interface.

## Table of Contents

1. [Overview](#overview)
2. [Exploit Description](#exploit-description)
3. [Usage](#usage)
4. [Vulnerable Devices](#vulnerable-devices)
5. [Disclaimer](#disclaimer)

## Overview

CVE-2023-46453 is a critical vulnerability in GL.iNet routers that allows attackers to bypass authentication mechanisms and access the router's web interface without proper credentials. This exploit script leverages the vulnerability to demonstrate unauthorized access.

## Exploit Description

The exploit script works by sending crafted requests to the affected router's web interface. It takes advantage of the lack of proper authentication checks in the `/usr/sbin/gl-ngx-session` file, allowing attackers to manipulate the username parameter to bypass authentication.

## Usage

To use this exploit script, follow these steps:

1. Clone this repository: `git clone https://github.com/0x1x02/GLiNet-Router-Auth-Bypass.git`
2. Navigate to the repository directory: `cd GLiNet-Router-Auth-Bypass`
3. Run the exploit script with the target URL as an argument: `python3 exploit.py https://target.com`

## Vulnerable Devices

The following GL.iNet router models running firmware version 4.3.7 are confirmed to be vulnerable:

- GL-MT3000
- GL-AR300M
- GL-B1300
- GL-AX1800
- GL-AR750S
- GL-MT2500
- GL-AXT1800
- GL-X3000
- GL-SFT1200
- And many more...

## Disclaimer

This exploit script is provided for educational and research purposes only. The author is not responsible for any misuse or damage caused by its usage. Use it at your own risk and only on authorized systems.
