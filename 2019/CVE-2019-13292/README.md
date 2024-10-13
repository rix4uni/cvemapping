# Blind SQL Injection Exploit for WebERP

This is a Python3 script that demonstrates an exploit for a Blind SQL Injection vulnerability in WebERP version 4.15, initially discovered by Semen Alexandrovich Lyhin on June 10, 2019. The original exploit can be found [here](https://www.exploit-db.com/exploits/47013), and further details regarding the WebERP system can be obtained from the official WebERP website.
Overview

## Overview

The vulnerability lies in the way WebERP handles queries received in base64 encoding and passed to the unserialize() function. Notably, the script can deserialize these queries into an array without any sanitization. After that, each element of this array is fed directly into the SQL query without further checks, leaving the system prone to SQL injection attacks.
Script Operation

## This Script

This script works by exploiting the above vulnerability in the following steps:

A malicious query is prepared using the generatePayload() function. The function designs a serialized array with SQL injection payloads and encodes it into base64 format.

The script logs in to the WebERP system using the provided credentials and the getCookies() function, which retrieves session cookies.

A new supplier is added to the system using the addSupplierID() function. The supplier's name is used later as a marker to identify the system's response.

The exploit is executed using the runExploit() function. It sends a POST request to the "Payments.php" page of the WebERP system. This function embeds the base64 encoded payload as a parameter in the POST data.

The response time to the request is measured. A significantly longer response time suggests that the SQL query was delayed due to the injected sleep() command, confirming the presence of the SQL injection vulnerability.
    
## Usage

```python
python3 exploit.py <target> <path> <login> <password> <order>
```

Replace `<target>`, `<path>`, `<login>`, `<password>`, and `<order>` with your target IP address, target path, user login, user password, and company order respectively.

Example:

```python
python exploit.py 192.168.1.1 'WEBerp/' admin weberp 1
```
