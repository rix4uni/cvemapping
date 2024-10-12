This script is designed to exploit vulnerabilities in a Mailcow instance using Cross-Site Scripting (XSS) and Remote Code Execution (RCE). The script aims to:

Inject an XSS payload into a Mailcow web interface.

Use the XSS payload to execute unauthorized actions.

Achieve RCE by overwriting a server template and executing commands.

Requirements


1. Python 3: Ensure Python 3 is installed on your machine. You can download it from the official website(https://www.python.org/downloads/).

 2. Requests Library: Install the requests library if it's not already installed. You can do this by running: 

   pip install requests

   3. Target Mailcow Instance: You need access to a Mailcow instance where you have identified a potential XSS vulnerability.

 
 Steps to Use the Script


1. Download the Script: Save the provided script in a Python file, e.g., exploit.py.

2. Run the Script: Execute the script in your terminal or command prompt. The script will prompt you for the target Mailcow instance URL.

 python3 exploit.py

3. Provide Target URL: When prompted, enter the URL of the target Mailcow instance. For example:

   Enter the target Mailcow instance URL (e.g., https://mail.mailcow.example): http://setted-domain/SOGo/so/rex@example.mail.com/Mail/view!/Mail/0/inbox

4. Monitor Output: The script will perform the following actions:

   - Send a malicious email containing the XSS payload.

   - Wait for the victim to open the email.

   - Send an API request to overwrite the rspamd maps.

   - Trigger the execution of the malicious code.

   - Log responses and indicate success or failure of each step.

   Find detailed CVE analysis at www.vsociety.io

