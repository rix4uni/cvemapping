# SSL Checker Script

This repository contains a Python script that checks the OpenSSL version on your system and tests SSL/TLS connections to a user-provided website. The script is designed to identify whether the system is affected by CVE-2021-4044 and to test the handling of SSL errors during the connection process.

## Features

- **OpenSSL Version Check:** The script checks the version of OpenSSL installed on your system and alerts you if it is vulnerable to CVE-2021-4044.
- **SSL Connection Test:** It attempts to establish an SSL connection to a website provided by the user, handling and reporting any SSL errors that occur.
- **User Input:** The script prompts the user to input the target website URL for the SSL connection test.

## Prerequisites

- **Python 3.x:** Ensure that you have Python 3 installed on your system.
- **Required Modules:** The script uses the following Python modules, which are part of the standard library:
  - `ssl`
  - `socket`

## Usage

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/phirojshah/CVE-2021-4044.git
    cd CVE-2021-4044
    ```

2. **Run the Script:**
    ```bash
    python3 ssl_check.py
    ```

3. **Enter Website URL:**
   When prompted, enter the URL of the website you want to check, for example:



4. **Review the Output:**
The script will output the OpenSSL version, whether it’s affected by CVE-2021-4044, and the result of the SSL handshake with the provided website.

## Example Output


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an Issue if you find a bug or have a feature request.

## Author

- **Your Name** - [Your GitHub Profile](https://github.com/phirojshah)

## Disclaimer

This script is intended for educational and ethical testing purposes only. Do not use this tool on systems or websites without proper authorization.

