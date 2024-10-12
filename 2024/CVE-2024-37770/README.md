# CVE-2024-37770

## description
14Finger v1.1 was discovered to contain a remote command execution (RCE) vulnerability in the fingerprint function. This vulnerability allows attackers to execute arbitrary commands via a crafted payload.

## Attack Vector
Unauthenticated attackers can execute command injection through shell metacharacters, thereby RCE remote servers.

## Detail
There is an unauthorized remote command execution vulnerability at the fingerprint scanning point of the core function
![image](https://github.com/k3ppf0r/CVE-2024-37770/assets/63085409/82375a33-0c6a-4634-a917-610a92359499)

Through the audit source code, you can see that when only_spider is false, spider is true, you will execute the crawl_site() function
![image](https://github.com/k3ppf0r/CVE-2024-37770/assets/63085409/c6d42a1d-10c5-4613-bfeb-1d0b3f2ecb67)

Continue to follow up, find that the submitted URL will be stitched to CMD, handed over to the subprocess module of Python for execution, and arbitrarily commands can be executed by constructing Payload.
![image](https://github.com/k3ppf0r/CVE-2024-37770/assets/63085409/e79919f3-9dd3-4b3d-a9d3-bd81a6a1883d)

Exploit:
![image](https://github.com/k3ppf0r/CVE-2024-37770/assets/63085409/d1264671-51d8-4473-8159-60afb5d0b60f)


The program is blocked, why? Because our command execution was successful!

![image](https://github.com/k3ppf0r/CVE-2024-37770/assets/63085409/5ae69370-a71c-4224-9d93-64c0c4c83378)

SUCCEED！
