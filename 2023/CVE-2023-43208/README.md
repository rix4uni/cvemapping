# CVE-2023-43208 - Mirth Connect Remote Code Execution (RCE) Exploit 🚨

## Introduction 📖

This repository contains a Proof-of-Concept (PoC) exploit for a critical vulnerability in NextGen Healthcare Mirth Connect versions prior to 4.4.1. The vulnerability, tracked as CVE-2023-43208, allows for unauthenticated remote code execution (RCE) on systems running the vulnerable software versions.

Mirth Connect, an open-source healthcare integration engine, failed to properly handle deserialized data, making it susceptible to arbitrary OS command execution through specially crafted HTTP requests. The vulnerability was discovered following an incomplete patch for CVE-2023-37679, initially addressed by IHTeam. Subsequent research by Horizon3.ai revealed a bypass to the deny list implemented in the original patch, leading to the identification of CVE-2023-43208. This exploit module has been successfully tested against Mirth Connect versions 4.1.1, 4.3.0, and 4.4.0.

## Disclaimer ⚠️

The provided Proof-of-Concept (PoC) and exploit code is for educational and research purposes only. Unauthorized testing and misuse of this PoC exploit against systems without explicit consent is illegal and strictly prohibited. The author assumes no responsibility for any misuse or damage caused by this tool.

By using this exploit, you agree to use it in an ethical and legal manner. Testing should only be performed on systems where explicit permission has been given.

## Prerequisites 🛠️

- Python 3.10 or higher
- `requests` Python library
- `pwncat-cs` Python library
- `rich` Python library

## Usage 💻

To use the exploit, clone this repository and navigate to the project directory. You can then run the exploit script as follows:

```bash
pip install -r requirements.txt
python3 CVE-2023-43208.py -u <Target URL> -lh <Listening Host> -lp <Listening Port>
```

Optional arguments include:

- `-f/--file` to specify a file containing target URLs for batch scanning.
- `-o/--output` to specify an output file for saving scan results.
- `-t/--threads` to set the number of threads for concurrent scanning.

## Features ✨

- Single target exploitation
- Batch scanning and exploitation from a file
- Customizable listening host and port for reverse shell connection
- Multi-threaded scanning capability
- Detailed console output with rich formatting

## Contribution 🤝

Contributions, feature requests, and suggestions are welcome! Please feel free to open issues or submit pull requests.

## Acknowledgments 🙏

- Original vulnerability discovery: IHTeam
- Patch analysis and CVE-2023-43208 discovery: Horizon3.ai

