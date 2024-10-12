# Ubuntu Privilege Escalation: CVE-2023-2640 and CVE-2023-32629

This is a local privilege escalation vulnerability affecting certain Ubuntu kernels. It allows unprivileged users to set privileged extended attributes on mounted files, bypassing security checks and potentially gaining elevated privileges. Two CVEs, CVE-2023-2640 and CVE-2023-32629, are associated with this vulnerability. The affected kernels include versions 6.2.0, 5.19.0, and 5.4.0, across various Ubuntu releases. It's crucial to apply patches provided by Ubuntu promptly and follow security best practices to mitigate these vulnerabilities.

## Usage

1. Make the script executable:
```bash
chmod +x poc.sh
```
2. Run the script:
```bash
./poc.sh
```
## Demo

[![Demo Video](https://img.youtube.com/vi/Up5q-FLWNk4/0.jpg)](https://www.youtube.com/watch?v=Up5q-FLWNk4)
