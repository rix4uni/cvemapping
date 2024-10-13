# boatcrash
Exploit for CVE-2019-19030 that affects Harbor versions &lt;1.10.3 and &lt;2.0.1. Can also be used to enumerate and pull public projects from higher versions.

---
## Requirements
This script requires the following dependencies:

- jq
- docker
- curl

For normal dependencies, you can use your package manager of choice:
```
sudo apt install jq curl
```

For Docker, please refer to Docker's instructions on [how to install Docker Engine](https://docs.docker.com/engine/install/) on your Unix-based OS of choice.

## Usage
```
$ ./boatcrash.sh <harbor_domain_name>
```
Use this script on Harbor instances running versions under 1.10.3 or 2.0.1 to enumerate all projects present in the platform.
It can also be used to enumerate projects on higher versions but you will only be able to enumerate **public** projects.

Any projects caught by this script will be pulled through docker into your own machine, where you will now be able to execute them locally and peruse environment variables and secrets.

### Disclaimer
This proof of concept exploit is intended solely for educational purposes and to help ethical hackers, security researchers, and organizations understand potential vulnerabilities in their systems. Users of this exploit must ensure they are in full compliance with all relevant local, state, national, and international laws. You must obtain explicit permission from the system owner before testing any systems using this exploit. This exploit is not intended to be used for any malicious activities, including but not limited to:
- unauthorized access;
- data theft;
- disruption of services;
- harming any individual or organization;
- etc.

I am publicizing this exploit, but I take no responsibility for any misuse or damage caused by the use of this exploit. Users assume all responsibility and liability for any actions taken with this exploit.
