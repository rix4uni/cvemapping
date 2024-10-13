
# CVE-2021-36396 Exploit

## Description
This repository holds a Python-based exploit targeting CVE-2021-36393, a severe vulnerability found within Moodle's recent courses feature. The flaw resides in the 'sort' parameter, enabling SQL injection attacks that can lead to unauthorized database access. Rated 9.8 on the CVSS scale, exploiting this vulnerability requires minimal privileges, such as a student role, and significantly compromises data confidentiality and integrity.

Affected Versions:
 - 3.11, 3.10 to 3.10.4, 3.9 to 3.9.7 and earlier unsupported versions

## Installation
To use this exploit, you need to have Python installed on your system. Clone this repository and install the required dependencies:

```bash
git clone https://github.com/T0X1Cx/CVE-2021-36393-Exploit.git
cd CVE-2021-36393-Exploit
pip install -r requirements.txt
```

## Usage
Run the exploit using the following command:

```bash
python3 exploit.py
```

**Note on Injection Point and Request Data Modification:**
The current implementation of this exploit is designed to extract the database name and the name and hash of the first user created in Moodle. Depending on your specific requirements or the target system, you may need to modify the injection point and the request data within the exploit code. This involves adapting the SQL injection payload and potentially altering the HTTP request format to match the target system's expectations. Careful analysis of the target system's behavior is required to tailor the exploit effectively.

## Disclaimer
This exploit is provided for educational and ethical testing purposes only. The use of this exploit for attacking targets without prior mutual consent is illegal. The author is not responsible for any damage caused by using this exploit.

## Credits
Exploit developed by Julio Ángel Ferrari (Aka. T0X1Cx)
