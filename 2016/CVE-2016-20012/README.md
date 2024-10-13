# CVE-2016-20012  SSH Username Enumeration Script

This Python script attempts to enumerate valid usernames on an SSH server by trying to connect with an invalid password. It measures the response time for each username to identify possible valid accounts based on server behavior.

## Table of Contents
- [Overview](#overview)
- [How It Works](#how-it-works)
- [Requirements](#requirements)
- [Setup and Usage](#setup-and-usage)
- [Disclaimer](#disclaimer)

## Overview

This script performs SSH username enumeration by leveraging the `paramiko` library. It attempts to connect to an SSH server using usernames from a provided wordlist and an invalid password. The response times for each attempt are collected, and the average and standard deviation of the response times are calculated.

This script can be useful for security researchers or penetration testers to check if certain usernames exist on the target system by identifying differences in server response times.

## How It Works

1. **SSH Client**: The script uses `paramiko.SSHClient()` to initiate an SSH connection to a specified hostname and port.
2. **Invalid Password**: For each username from the wordlist, the script tries to authenticate with an invalid password.
3. **Response Time**: The time taken for each connection attempt is recorded.
4. **AuthenticationException**: The script expects an `AuthenticationException` when using an invalid password. If other errors occur, they are reported and the script stops.
5. **Statistics**: For each username, the script calculates the average response time and standard deviation over multiple attempts.

## Requirements

To run this script, you need to have the following installed on your machine:

- Python 3.x
- The following Python libraries:
  - `paramiko`
  - `statistics`
  - `os`
  - `time`

You can install the necessary dependencies using the following command:

```bash
pip install paramiko

