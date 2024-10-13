# CVE-2018-19410-POC
Proof of concept for the vulnerability CVE-2018-19410
# Details
PRTG Network Monitor
Version: 18.2.39.1661 and earlier 

Severity level: High
Impact: Authentication Bypass, Improper Authorization, Local File Inclusion
Access Vector: Remote

The vulnerability permits remote and unauthenticated attackers to generate users with read-write privileges, including administrative access. This is achieved by manipulating attributes within the 'include' directive found in the /public/login.htm file, allowing the inclusion and execution of a "/api/addusers" file.

# Usage
python3 CVE-2018-19410-POC.py target_ip username<br/>
Example: CVE-2018-19410-POC.py 10.10.10.10 test_user
