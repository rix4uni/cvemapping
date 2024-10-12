## CVE-2023-50564 (PoC)

This repository contains a Proof of Concept for CVE-2023-50564 vulnerability in Pluck CMS version 4.7.18

## Description

CVE-2023-50564 is a vulnerability that allows unauthorized file uploads in Pluck CMS version 4.7.18. This exploit leverages a flaw in the module installation function to upload a ZIP file containing a PHP shell, thereby enabling remote command execution.

## Usage

### Prerequisites

- Python 3.x
- The `requests` and `requests_toolbelt` packages

You can install the necessary packages with the following command:

```bash
pip install requests requests_toolbelt
```
## Instructions
1. Clone this repository:

```bash
git clone https://github.com/Rai2en/CVE-2023-50564_Pluck-v4.7.18_PoC.git
cd CVE-2023-50564_Pluck-v4.7.18_PoC
```

2. Replace <hostname> with the target domain name or IP address in the PoC script.

3. Create a `payload.zip` file containing `shell.php`. I recommand [pentestmonkey](https://github.com/pentestmonkey/php-reverse-shell) PHP reverse shell and replace `<your_ip>` and `<port>` fields with your IP and listening port.

4. Run the PoC script:

```bash
python exploit.py
```
You will be prompted to enter the path to the ZIP file:
```bash
ZIP file path: ./path/to/payload.zip
```
## Output example 

- If the login and upload are successful:

```bash
Login account
ZIP file download.
<output of the executed shell.php>
```

- If a login error occurs:

```bash
Login problem. response code: <code>
```

- If an upload error occurs:

```bash
ZIP file download error. Response code: <code>
```

## Note 
Ensure that the `shell.php` file contains the correct reverse shell and your listener is waiting for the connection on the specified port.
