# [CVE-2024-26581] Vulnerability Checker for BGN Internal

## Requirements
- Bash
- Wget

## Installation
- Make sure to download and place the tool in the ``/opt/`` directory.
- Download the tool source code by running the command: ``sudo wget https://raw.githubusercontent.com/madfxr/CVE-2024-26581-Checker/main/CVE-2024-26581.sh`` and ``sudo wget https://raw.githubusercontent.com/madfxr/CVE-2024-26581-Checker/main/CVE-2024-26581-Manual.sh``.
- Grant access rights to the ``/opt/CVE-2024-26581.sh`` file by running the command: ``sudo chmod +x CVE-2024-26581.sh`` and ``sudo chmod +x CVE-2024-26581-Manual.sh``.
- Running this tool with a command ``./CVE-2024-26581.sh`` and ``./CVE-2024-26581-Manual.sh``

## References
- CVE: https://nvd.nist.gov/vuln/detail/CVE-2024-26581
- PoC: https://github.com/google/security-research/tree/master/pocs/linux/kernelctf/CVE-2024-26581_lts_cos_mitigation
