# CVE-2022-47909 - Unauthenticated Arbitrary File Deletion
This exploit abuses two CVEs in Checkmk <= 2.1.0p11, Checkmk <= 2.0.0p28, and all versions of Checkmk 1.6.0 (EOL) to achieve unauthenticated arbitrary file deletion.

* **CVE-2022-48321** - An SSRF vulnerability in the Agent_Receiver endpoint of the CheckMK software. By abusing the vulnerable /register_with_hostname endpoint, we can cause a blind SSRF.
* **CVE-2022-47909** - Through our blind SSRF we can abuse a line feed injection in the /ajax_graph_images.py endpoint to initiate an attacker controlled LQL query. This injection can be used to extract data, or to run Nagios External Commands.

This exploit uses the SSRF + LQL injection combination for an arbitrary file deletion vulnerability. This exploit can be chained with other exploits in the vulnerable versions for unauthenticated remote code execution as described in the following series of articles: https://www.sonarsource.com/blog/checkmk-rce-chain-1/

DISCLAIMER: This script is made to audit the security of systems. Only use this script on your own systems or on systems you have written permission to exploit.
