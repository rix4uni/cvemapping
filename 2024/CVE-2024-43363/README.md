# CVE-2024-43363

CVE-2024-43363 Exploit Script

This Python script is designed to test if a Cacti instance is vulnerable to CVE-2024-43363, a Remote Code Execution (RCE) vulnerability caused by log poisoning.
How the Vulnerability Works:

    Log Poisoning: An attacker injects PHP code into device names, which gets logged by Cacti without proper sanitization.
    Execution: By accessing the logs via a web URL, the injected code is executed, allowing the attacker to run commands on the server.

How the Script Operates:

    Check Version: The script checks if the target Cacti version is vulnerable.
    Create Malicious Device: It attempts to create a device with a PHP code-injected name.
    Check Logs: The script checks if the code appears in the logs and could be executed.

Requirements:

    Python 3.x
    requests library: Install with pip install requests

Usage:

    Clone the repository and navigate to the folder.
    Edit the url and token variables in the script to match your target.
    Run the script:

    bash

python3 cacti_exploit.py
