# CVE-2025-46047
## Silverpeas <= 6.4.2 Username Enumeration PoC
Proof-of-Concept script for demonstrating a username enumeration vulnerability in Silverpeas versions 6.4.1 and 6.4.2.

## Vulnerability Details

* **Affected Software:** Silverpeas
* **Affected Versions:** 6.4.1, 6.4.2 (and potentially earlier versions)
* **Fixed Version:** 6.4.3
* **Vulnerability Type:** Username Enumeration via Observable Response Discrepancy (CWE-204)
* **Vendor Tracking ID:** Silverpeas Bug #14829

**Summary:** The vulnerability exists in the forgot password functionality (`/silverpeas/CredentialsServlet/ForgotPassword` endpoint). By sending POST requests with potential usernames in the `Login` parameter, the server responds with different HTTP status codes (200 OK for valid users, 302 Found for invalid users). This discrepancy allows a remote, unauthenticated attacker to determine valid usernames on the system.

## Proof-of-Concept (PoC) Script

* **Script Name:** `silverpeas_enum_poc.py`
* **Description:** This Python script automates the process of sending requests to the vulnerable endpoint with usernames (provided individually or from a wordlist) and identifies potentially valid/invalid accounts based on the server's HTTP status code response.

## Usage

### Requirements

* Python 3.x
* `requests` library (`pip install requests`)

### Instructions

1.  Clone the repository or download the script (`silverpeas_enum_poc.py`).
2.  Install dependencies: `pip install requests`
3.  Run the script from your terminal:

    * **Test a single username:**
        ```bash
        python silverpeas_enum_poc.py <TARGET_URL> -u <USERNAME>
        ```
        *Example:* `python silverpeas_enum_poc.py http://vulnerable-silverpeas.local -u admin`

    * **Test usernames from a file:**
        ```bash
        python silverpeas_enum_poc.py <TARGET_URL> -w <WORDLIST_FILE>
        ```
        *Example:* `python silverpeas_enum_poc.py https://vulnerable-silverpeas.com -w users.txt`

### Output

The script will output:
* `[+] Username '...' appears VALID (Status: 200)` for usernames likely corresponding to existing accounts.
* `[-] Username '...' appears INVALID (Status: 302)` for usernames likely not corresponding to existing accounts.

## Disclaimer

This script is provided for educational purposes and for demonstrating the vulnerability. Use this script responsibly and only against systems you have explicit, written authorization to test. Unauthorized scanning or testing is illegal and unethical. The author assumes no liability and is not responsible for any misuse or damage caused by this script.

## Author / Credit

* **Shantanu Saxena / j0ey17**

## Disclosure Timeline

* **Discovered:** 08/04/2025
* **Reported to Vendor (Silverpeas):** 08/04/2025
* **Vendor Acknowledged / Assigned ID (#14829):** 09/04/2025
* **Patch Released (Version 6.4.3):** 11/04/2025
* **PoC Published:** 14/04/2025
* **CVE ID: CVE-2025-46047**

## References
* **[(Vendor Fix PR)](https://github.com/Silverpeas/Silverpeas-Core/pull/1399)**
