# CVE-2015-57115
Mass Checker For CVE-2015-57115 

## Description

The CVE-2015-57115 Checker Script is a Python tool for detecting vulnerabilities related to CVE-2015-57115, which is a path traversal vulnerability in certain PHP applications. The script checks multiple URLs for the presence of this vulnerability by sending requests with crafted payloads.

## Features

- **Payload Checking**: Tests various payloads to check for path traversal vulnerabilities.
- **Multi-threading**: Supports concurrent URL checks to speed up the process.
- **Configurable Timeout and Retries**: Allows setting request timeout and number of retries.
- **Output File**: Saves the results of the vulnerability checks to an output file.
- **Colorful Output**: Provides clear, color-coded terminal output for easy interpretation of results.

## Requirements

- Python 3.x
- `requests` library
- `colorama` library

You can install the required libraries using pip:

```bash
pip install requests colorama
```

## Usage

### Check a Single URL

To check a single URL, use the following command:

```bash
python CVE-2015-57115.py --url http://example.com --timeout 10 --threads 5 --retries 3 --output results.txt
```

### Check URLs from a File

To check multiple URLs from a file, use:

```bash
python CVE-2015-57115.py --file urls.txt --timeout 10 --threads 5 --retries 3 --output results.txt
```

### Arguments

- `--url`: Single URL to check.
- `--file`: File containing multiple URLs to check (one URL per line).
- `--timeout`: Request timeout in seconds (default: 10).
- `--threads`: Number of threads for parallel URL checks (default: 5).
- `--retries`: Number of retries for failed requests (default: 3).
- `--output`: File to write the results of the vulnerability checks.

## Output

The script will print the results to the terminal and save them to the specified output file. The output includes:

- The URL being checked.
- The result of the check (Vulnerable or Not Vulnerable).
- Details about any issues encountered during the check.

At the end of the run, the script will display the total number of vulnerable URLs and confirm the file where results were saved.

## Example

```bash
python CVE-2015-57115.py --file urls.txt --threads 5 --output vulnerable_urls.txt
```

## Contact: @zpgod (Telegram)
