# CVE-2022-30525_check

Description:
This script checks for the presence of the OS command injection vulnerability (CVE-2022-30525) in Zyxel USG FLEX devices running firmware versions 5.00 through 5.21 Patch 1. The vulnerability allows an attacker to modify specific files and execute OS commands on a vulnerable device.

Instructions for use:

- Ensure that Python 3 is installed on your system
- Download the script and save it to your local machine
- Open a command prompt or terminal window and navigate to the directory where the script is saved
- Run the script with the following command: "python CVE-2022-30525.py -t [TARGET_URL]"
- Replace [TARGET_URL] with the URL of the Zyxel USG FLEX device you wish to check
- The script will check the device for the vulnerability and print the result to the console.

Note:

- Make sure the device is reachable and you have the correct URL
Script will check for the vulnerability by sending a specific request with headers, it will check if the request get a 200 status code and if the headers contain a specific string, if not it will be considered safe.
