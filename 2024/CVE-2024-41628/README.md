# CVE-2024-41628

Simple exploit script developed by Redshift Cyber Security to exploit (CVE-2024-41628) ClusterControl LFI vulnerability.

The vulnerability affects the CMON API and specifically the RPC and RPC-TLS user interfaces which by default reside on port 9500 and 9501 respectively.

Due to ClusterControl also typically running as root, any system file can be retrieved.

Examples of files to retrieve:
- /etc/shadow
- /etc/passwd
- /root/.ssh/id_rsa
- /etc/cmon.cnf - (Contains ClusterControl RPC Key) 

Affected versions of ClusterControl are 1.9.8 before 1.9.8-9778, 2.0.0 before 2.0.0-9779, and 2.1.0 before 2.1.0-9780.

## Usage: 
```python
python3 CVE-2024-41628.py ip port file
```
## Help: 
```python
python3 CVE-2024-41628.py -h
```
## Example: 
```python
python3 CVE-2024-41628.py 127.0.0.1 9500 /etc/shadow
```
