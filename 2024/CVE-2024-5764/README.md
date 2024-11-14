# CVE-2024-5764

This repository contains a Python script capable of exploiting [CVE-2024-5764](https://www.cve.org/CVERecord?id=CVE-2024-5764) by decrypting encrypted data with the static encryption key. Sonatype announcement available [here](https://support.sonatype.com/hc/en-us/articles/34496708991507-CVE-2024-5764-Nexus-Repository-Manager-3-Static-hard-coded-encryption-passphrase-used-by-default-2024-10-17).

## Usage

```
usage: cve-2024-5764.py [-h] [-e ENCRYPTED_PAYLOAD] [-p PASSPHRASE]

Decrypt data encrypted by the Java PasswordCipher class (CVE-2024-5764).

options:
  -h, --help            show this help message and exit
  -e ENCRYPTED_PAYLOAD, --encrypted_payload ENCRYPTED_PAYLOAD
                        Base64 encoded encrypted payload.
  -p PASSPHRASE, --passphrase PASSPHRASE
                        Passphrase used to decrypt the payload.
```

## Disclaimer

This program is intended for legitimate and authorized purposes only. The author holds no responsibility or liability for misuse of this project.
