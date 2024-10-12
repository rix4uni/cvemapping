# Exim CVE-2024-39929 Exploit PoC

This repository contains a Proof-of-Concept (PoC) script to exploit the Exim vulnerability CVE-2024-39929. The vulnerability affects Exim versions prior to 4.98, allowing attackers to bypass file extension blocking mechanisms and potentially deliver executable attachments to users' mailboxes.

## Description

The PoC script in this repository reads a list of SMTP servers from an external file and sends an email with a crafted attachment designed to exploit CVE-2024-39929. The script dynamically sets the email subject to indicate the server through which the email was passed.

## Usage

### Prerequisites

- Python 3.x
- `smtplib` and `email` modules (standard with Python)

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/michael-david-fry/CVE-2024-39929.git
    cd CVE-2024-39929
    ```

2. Ensure you have a file named `servers.txt` in the repository directory. This file should contain a list of IP addresses or FQDNs, each on a new line.

### Running the Script

1. Execute the script, providing the path to `servers.txt` as a command-line argument:
    ```sh
    python CVE-2024-39929_POC.py path/to/servers.txt
    ```

2. The script will prompt you for the sender and recipient email addresses:
    ```plaintext
    Enter the sender email address: sample@test.com
    Enter the recipient email address: sample@test.com
    ```

### Example

```sh
python CVE-2024-39929_POC.py servers.txt
```

Example prompts:
```plaintext
Enter the sender email address: sample@test.com
Enter the recipient email address: sample@test.com
```

## Script Details

The script performs the following actions:
1. Reads the list of SMTP servers from the specified file.
2. Prompts the user for sender and recipient email addresses.
3. Connects to each SMTP server on port 25.
4. Sends an email with a crafted attachment designed to exploit CVE-2024-39929.
5. Sets the email subject to indicate the server used for sending the email.
6. Prints debug information and handles exceptions.

## Important Considerations

- **Ports**: This PoC was designed for port 22 only, but can be tailored to include additional ports (465, 587, etc.) on line 78.
- **Ethical Use**: Ensure you have permission to test these servers for vulnerabilities. Unauthorized testing can be illegal and unethical.
- **Monitoring**: Monitor the responses and behaviors of the servers to determine if the exploit was successful.
- **Temp Email Host**: Using an email host that does not scan for malware is essential, otherwise other security controls will interfere. https://www.guerrillamail.com/

## References
- https://thehackernews.com/2024/07/critical-exim-mail-server-vulnerability.html
- https://nvd.nist.gov/vuln/detail/CVE-2024-39929
- https://github.com/Exim/exim
- https://github.com/rxerium/CVE-2024-39929

## Disclaimer

This tool is intended for educational purposes and authorized testing only. The authors are not responsible for any misuse of this tool.

## Contact

For issues, questions, or contributions, please create an issue or submit a pull request on the [GitHub repository](https://github.com/michael-david-fry/CVE-2024-39929).
