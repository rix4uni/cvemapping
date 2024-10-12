# CVE-2023-20273
CVE-2023-20273 Exploit PoC

## Usage
```
usage: exploit.py [-h] -t URL -u Username -p Password (-c Command | -r) [-dest Outfile] [-www | -tcp | -null] [-ip LocalIP] [-port LocalPort] [-fs filesystem] [-path filepath] [-operation operation_type] [-v] [-q]

CVE-2023-20273 Exploit PoC

options:
  -h, --help                    show this help message and exit

Target options:
  [Mandatory] Target arguments

  -t URL, --url URL             Target Cisco URL (eg https://192.168.1.1 or http://192.168.2.2:8080)
  -u Username, --user Username  Cisco webui user name
  -p Password, --pass Password  Cisco webui user pass

Exploit mode:
  [Mandatory] Exec command or reverse shell

  -c Command                    Command to run
  -r                            Reverse shell (requires -ip and -port)

Output Options:
  [Optional] Command output options

  -dest Outfile                 [-r | -www | -tcp] destination file (default: random)
  -www                          [Default] Attempt to retrieve output via target web server
  -tcp                          [Not implemented] Attempt to send output to a TCP listener (requires -ip and -port)
  -null                         Do not attempt to get command output

Callback Options:
  For reverse shell or command output

  -ip LocalIP                   Local IP for reverse shell/command output
  -port LocalPort               Local port for reverse shell/command output

Exploit options:
  [Not implemented] Exploit modifiers

  -fs filesystem                Filesystem on target for exploit staging (default: flash)
  -path filepath                Filepath on target filesystem for exploit staging (default: shellsmoke)
  -operation operation_type     Install operation type (not currently implemented) (default: SMU)

Verbosity control:
  -v                            Verbose output
  -q                            Suppress Banner
```
