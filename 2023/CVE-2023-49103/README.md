# CVE-2023-49103
PoC for the CVE-2023-49103

## Overview
This Python script is designed to efficiently process a large list of URLs to check for the presence of `phpinfo()` output. It uses multi-threading to handle a large number of URLs concurrently, significantly speeding up the process. The script also features a real-time progress bar to visually track the progress.

To trigger the vulnerability, access to the phpinfo() URL isn't enough: you also need to bypass .htaccess (thanks rapid7 for the insight). In this case, this is done by adding /.css to the URL. 

## Requirements
- Python 3.x
- `requests`
- `urllib3`
- `colorama`
- `alive-progress`
- `concurrent.futures` (part of the standard library in Python 3)

## Installation
1. Ensure you have Python 3 installed on your system.
2. Clone this repository or download the script.
3. Install the required Python packages:

`pip install requests urllib3 colorama alive-progress`

## Usage
To use the script, you need a text file containing a list of URLs to check. Each URL should be on a new line.

## Prepare your URL list

Create a text file (e.g., urls.txt) with each URL on a new line.

## Run the script

Use the script with the following command, replacing input_file.txt with your file of URLs and output_file.txt with the desired output file name:

`python exploit.py -t input_file.txt -o output_file.txt`

## View Results

The script will process each URL and output the results to the specified output file. URLs with valid phpinfo() output are logged in this file.

##  Contributions
Feel free to fork this repository or submit pull requests with improvements.

Thanks @random-robbie for the PR <3 

##  Disclaimer 

I originally wrote this script just for fun (I was bored and wanted to try my hand at multithreading) and not for any malicious purposes. Do the same, test on YOUR own instances and not on the neighbor's instance. 
This script is ONLY for educational purposes, of course.  
