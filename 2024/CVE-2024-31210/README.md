# CVE-2024-31210
---

## WordPress Vulnerability Checker

This Ruby script checks if a given WordPress site is vulnerable to CVE-2024-31210, which allows administrator-level users on single-site installations and Super Admin-level users on Multisite installations to execute arbitrary PHP code via the plugin upload mechanism.

### Features
- Prompts the user to input the URL of the WordPress site to check.
- Sends an HTTP GET request to the specified URL.
- Analyzes the server's response to determine if the site is vulnerable.

### Usage
1. Clone the repository or download the script file.
2. Run the script using Ruby:
   ```sh
   ruby CVE-2024-31210.rb
   ```
3. Enter the URL of the WordPress site when prompted.

---
