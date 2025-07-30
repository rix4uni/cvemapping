EDNS Client Subnet (ECS) Remote Detection Tool - CVE-2025-40766

This tool checks whether a remote DNS resolver supports **EDNS Client Subnet (ECS)** — a DNS extension that may expose systems to cache poisoning or information leakage vulnerabilities such as **CVE-2025-40766**.

## 🔍 What It Does

- Sends a DNS query with an ECS option
- Detects whether ECS is enabled on the target DNS resolver
- Compatible with both Linux/macOS (Python) and Windows (PowerShell)

## 💻 Usage (Python)

### Install dependencies:
```bash
pip3 install -r requirements.txt
```

### Run the script:
```bash
python3 ecs_checker.py <DNS_SERVER_IP>
```

### Examples:
```bash
python3 ecs_checker.py 1.1.1.1
[-] 1.1.1.1 does NOT support ECS (CLIENT-SUBNET not found).

python3 ecs_checker.py 8.8.8.8
[+] 8.8.8.8 supports ECS (CLIENT-SUBNET found).
```
