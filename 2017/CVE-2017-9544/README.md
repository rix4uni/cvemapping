# CVE-2017-9544

Exploit for SEH based buffer overflow in Easy Chat Server (CVE-2017-9544)

Based on:
* pwntools
* msfvenom / reverse\_tcp payload
* ropper
* x64dbg

Vulnerable app available at https://www.exploit-db.com/exploits/42155

## Setup

* Set victim IP to 192.168.15.100 and start Easy Chat Server.
* Set attacker IP to 192.168.15.101 and run `python main.py`
* Wait for reverse shell
