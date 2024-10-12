# CVE-2024-43917

This script demonstrates an SQL injection vulnerability found in the TI WooCommerce Wishlist plugin for WordPress, versions up to 2.8.2 (CVE-2024-43917). The vulnerability allows unauthenticated users to execute arbitrary SQL commands on the website’s database, potentially exposing sensitive information such as usernames and passwords.
Usage

Install the required Python dependencies:

bash

pip install requests

Replace the target_url in the script with the vulnerable site’s URL.

Run the script:

bash

    python exploit.py

Disclaimer

This script is for educational purposes only. Use only on systems you have explicit permission to test.
