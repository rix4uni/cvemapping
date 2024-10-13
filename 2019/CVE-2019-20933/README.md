# InfluxDB Exploit CVE-2019-20933

Exploit for InfluxDB CVE-2019-20933 vulnerability, InfluxDB before 1.7.6 has an authentication bypass vulnerability in the authenticate function in services/httpd/handler.go because a JWT token may have an empty SharedSecret (aka shared secret).
Exploit check if server is vulnerable, then it tries to get a remote query shell. It has built in a username bruteforce service.

## Installation
```
git clone https://github.com/LorenzoTullini/InfluxDB-Exploit-CVE-2019-20933.git
cd InfluxDB-Exploit-CVE-2019-20933
pip install -r requirements.txt
```

## Usage
```
python __main__.py
```
