# CVE-2019-16172
The CVE-2019-16172 Scanner is designed to check LimeSurvey instances for the stored XSS vulnerability.


## CVE Descriptions
### CVE-2019-16172
Description: CVE-2019-16172 is a stored XSS vulnerability found in LimeSurvey versions prior to 3.17. The vulnerability arises due to improper validation of user inputs when creating survey groups. An attacker can exploit this vulnerability by submitting a specially crafted payload, which can be stored on the server and executed in the context of other users accessing the survey.

Impact: Successful exploitation allows an attacker to execute arbitrary JavaScript in the context of the application, leading to potential data exfiltration, session hijacking, and other malicious activities.

## Scanner Descriptions
### CVE-2019-16172 Scanner
The CVE-2019-16172 Scanner is designed to check LimeSurvey instances for the stored XSS vulnerability. It sends a crafted payload to the /admin/survey/group/create endpoint and evaluates the response to determine if the server is vulnerable.

## Usage:

### Command: python cve_2019_16172_scanner.py --url <target_url>
#### Options:
--url: Specify a single URL to scan.
--file: Provide a file with multiple URLs for batch scanning.
--timeout: Set the request timeout (default is 10 seconds).
--threads: Specify the number of parallel threads for scanning (default is 5).
--output: Save results to a specified output file.



### Follow Us on Telegram
Stay updated with the latest tools and hacking resources. Join our Telegram Channel by clicking the logo below:

[![Telegram](https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Telegram_logo.svg/240px-Telegram_logo.svg.png)](https://t.me/Trixsec)
