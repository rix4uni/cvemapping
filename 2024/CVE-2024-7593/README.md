# CVE-2024-7593 Exploit Script

This Bash script serves as a proof of concept (PoC) for exploiting the authentication bypass vulnerability in Ivanti vTM (CVE-2024-7593). It allows users to create a new admin user on the target system.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Usage](#usage)
- [Parameters](#parameters)
- [Example](#example)
- [Author](#author)
- [License](#license)

## Prerequisites

Make sure you have the following installed on your system:

- curl: This script uses `curl` to send HTTP requests.

You can check if curl is installed by running:

``bash
command -v curl``


If it's not installed, you can install it using your package manager. For example, on Ubuntu:

``sudo apt-get install curl``

## Usage
To run the script, change permissions to +x and use the following command:

``./CVE-2024-7593.sh -u <host> -p <port>``


``<host>``: The target host (e.g., example.com).

``<port>``: The target port (e.g., 9090).


## Example

``./CVE-2024-7593.sh -u example.com -p 9090``


<img src="https://i.imgur.com/uP5WGqB.png" alt="CVE-2024-7593 PoC Screenshot" />

## Response Handling
If the new user is successfully created, the script will display the login credentials.
If the user creation fails, it will inform you of the failure.



## Author
D3N14LD15K&nbsp;&nbsp;&nbsp;:::&nbsp;&nbsp;&nbsp;D3N14LD15K[at]BUGCROWDNINJA.COM&nbsp;&nbsp;&nbsp;:::&nbsp;&nbsp;&nbsp;X.COM/D3N14LD15K



## Disclaimer
This proof of concept is for educational purposes only. You are responsible for your own use of this script.
