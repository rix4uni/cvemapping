# Poc LiteSpeed Cache CVE-2024-44000 Exploit
CVE-2024-44000 is a vulnerability in the LiteSpeed Cache plugin, a popular WordPress plugin. This vulnerability affects session management in LiteSpeed Cache, allowing attackers to gain unauthorized access to sensitive data.

------------------------------------------------------
![Proof of Concept](Poc%20CVE-2024-44000.jpg)
------------------------------------------------------

The script works in the following steps:
1. **Extract Cookies from Debug Log**: 
- The script sends a `GET` request to retrieve the `debug.log` file (`wp-content/debug.log`) from the server.
- It uses regular expressions to extract cookies from the file's contents.

2. **Extract Session Cookies**: 
- It filters the extracted cookies to locate session cookies matching the pattern: 
      ```
      wordpress_logged_in_[^=]+=[^;]+
      ```

3. **Hijack Admin Session**: 
- The script generates URLs with the stolen cookies and sends a `GET` request to the WordPress admin dashboard (`wp-admin/`).
- If the response includes a `302 Redirect` with a `Location` header containing the `wp-admin` path, it considers the hijacking successful.

## Factors Affecting Script Success
Several factors influence the effectiveness of this script:
- **Debug Log File Accessibility**: The script assumes that the `debug.log` file is publicly accessible and contains session cookies. If this is not the case, the script will not work.
- **Cookie Extraction and Filtering**: The regular expressions used for extracting cookies may not catch all possible formats or variations of session cookies.

## Disclaimer

**Important:** Exploiting vulnerabilities without permission is illegal and unethical. This script is intended for **educational and testing purposes only**. Use it only with explicit consent from the system owner.

