

# CVE-2023-28432 - PoC

## Description
This python3 script is designed to exploit CVE-2023-28432, which potentially affects certain MinIO server configurations. The script makes a POST request to a specified hostname, attempting to retrieve sensitive environment variables such as `MINIO_ROOT_PASSWORD` and `MINIO_UPDATE_MINISIGN_PUBKEY`.

## Requirements
- Python 3
- `requests` library

## Installation
Before running the script, ensure you have Python 3 installed on your system. You can install the required Python packages using pip:

```bash
pip3 install requests
```

## Usage
The script accepts the hostname as a required argument and has options for using HTTPS and printing raw data.

```bash
python3 exploit.py [hostname] [--use-https] [--raw]
```

### Arguments
- `hostname`: Specifies the target hostname, e.g., 'domain.htb'.
- `--use-https`: Enable this option to use HTTPS for the requests. The default is HTTP.
- `--raw`: Print the raw JSON data retrieved from the server.

## Example
To run the script against `example.htb` using HTTPS and print formatted environment variables:

```bash
python3 exploit.py example.htb --use-https
```

To print the raw JSON response:

```bash
python3 exploit.py example.htb --use-https --raw
```

## Note
This tool is for educational and ethical testing purposes only. Unauthorized testing of servers without explicit permission is illegal and unethical.
