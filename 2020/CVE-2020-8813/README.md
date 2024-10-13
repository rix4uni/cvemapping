# CVE-2020-8813 - RCE through graph_realtime.php in Cacti 1.2.8 

## Features

 - [x] 

## Description 

graph_realtime.php in Cacti 1.2.8 allows remote attackers to execute arbitrary OS commands via shell metacharacters in a cookie, if a guest user has the graph real-time privilege.

## Usage

```
$ ./CVE-2020-8813.py -h
PoC of CVE-2020-8813 - RCE through graph_realtime.php in Cacti 1.2.8 - by @podalirius_

usage: CVE-2020-8813.py [-h] -t TARGET [-v] [-u USERNAME] [-p PASSWORD] (-L | -c COMMAND) [-k]

options:
  -h, --help            show this help message and exit
  -t TARGET, --target TARGET
                        Target URL of the cacti
  -v, --verbose         Verbose mode. (default: False)
  -u USERNAME, --username USERNAME
                        Username to connect to Cacti
  -p PASSWORD, --password PASSWORD
                        Password to connect to Cacti
  -L, --live            Live mode. (default: False)
  -c COMMAND, --command COMMAND
                        Execute a single command
  -k, --insecure        Allow insecure server connections when using SSL (default: False)

```

## References
 - https://nvd.nist.gov/vuln/detail/CVE-2020-8813
 - https://github.com/Cacti/cacti/issues/3285