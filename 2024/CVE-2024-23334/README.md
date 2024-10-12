# CVE-2024-23334-PoC
A proof of concept of the LFI vulnerability on aiohttp 3.9.1. The option 'follow_symlinks' can be used to determine whether to follow symbolic links outside the static root directory. When 'follow_symlinks' is set to True, there is no validation to check if reading a file is within the root directory. This can lead to directory traversal vulnerabilities, resulting in unauthorized access to arbitrary files on the system.

# Usage

```bash
bash lfi.sh -u target_url -f File_to_Read
```

![imagen](https://github.com/user-attachments/assets/5b1e9449-d720-4982-81af-571aca45dbd2)

# Example

![imagen](https://github.com/user-attachments/assets/8730b3ce-cf55-4be0-9a71-34ff3321f4d4)
