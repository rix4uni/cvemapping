# CVE-2022-46196


## Description
This Python code exploits an unauthenticated command injection vulnerability in Cacti versions up to and including 1.2.22. It uses argparse to parse arguments from the command line, requests to get the HTML content of a target Cacti instance, and BeautifulSoup to extract the version number of Cacti from the HTML content. If the version is <= 1.2.22, the code proceeds with the exploit.

The exploit involves sending a payload to the remote_agent.php file of the Cacti instance, with the payload being a Bash command that opens a reverse shell to a specified listening IP and port. The code iterates through a range of host IDs to send the payload to, and once successful, opens a reverse shell on the specified IP and port.

This code should only be used for ethical purposes, such as security research or penetration testing.

## Usage
To run the code, use the following command:

```bash
python exploit.py --url <URL of Cacti's instance> --lhost <Listening IP> --lport <Listening Port>
```

Where:

- URL of Cacti's instance is the URL of the target Cacti instance.
- Listening IP is the IP address on which the reverse shell should listen.
- Listening Port is the port on which the reverse shell should listen.

## Required Python Libraries/Modules
The code requires the following Python libraries/modules:

```
argparse
requests
BeautifulSoup4
re
```
