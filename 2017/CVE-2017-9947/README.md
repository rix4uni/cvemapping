# :cyclone: APOLOGEE - Siemens Field Panel Scanner:

APOLOGEE is a Python script and Metasploit module that enumerates a hidden directory on Siemens APOGEE PXC BACnet Automation Controllers (all versions prior to V3.5) and TALON TC BACnet Automation Controllers (all versions prior to V3.5). With a 7.5 CVSS, this exploit allows for an attacker to perform an authentication bypass using an alternate path or channel to access hidden directories in the web server.  This repository takes advantage of CVE-2017-9947.

<p align="center">
  <img width="600" alt="PXCM" src="https://user-images.githubusercontent.com/72598486/170399536-2ac18d9a-ba50-41a8-95ae-c17d42f59d63.png">
</p>

# What are Siemens Field Panels?

Siemens Field Panels primarily provide process controls for Building automation systems (BAS). A building automation system (BAS) is a network designed to connect and automate certain functions inside a building. All of the building control systems, from lighting and HVAC (Heating, Ventilation & Air Conditioning) to fire and security systems—all wired through one set of controls. So what does this mean? By using the APOLOGEE repository, you can enumerate the devices controlling building automation processes for information on their locations, configurations, and much more!


# Demo:

https://user-images.githubusercontent.com/72598486/170400132-732e5e86-bde1-4117-a0ff-aef043a3a2cd.mp4

# CVE:

An attacker with network access to the integrated web server (Ports 80/TCP and 443/TCP) could bypass the authentication and download sensitive information from the device.

A directory traversal vulnerability could allow a remote attacker with network access to the integrated web server (Ports 80/TCP and 443/TCP) to obtain information on the structure of the file system of the affected devices.

<img width="1268" alt="CVE" src="https://user-images.githubusercontent.com/72598486/170395925-58f67eb6-f5c3-48f3-9765-20b81bf6886d.png">

## Details:

- **Vulnerabilities:** Authentication Bypass Using an Alternate Path or Channel, Path Traversal
- **CVSS v3:** 7.5
- **Vendor:** Siemens
- **Equipment:** BACnet Field Panels
- **Products:** APOGEE PXC BACnet Automation Controllers: All versions prior to V3.5 and TALON TC BACnet Automation Controllers: All versions prior to V3.5

## Mitigation:

Siemens has provided firmware Version V3.5 for BACnet Field Panels Advanced modules, which fixes the vulnerabilities, and they recommend that users update to the new fixed version. Users should contact the local service organization for further information on how to obtain and apply V3.5. The web form is available at the following location on the Siemens web site:

http://w3.usa.siemens.com/buildingtechnologies/us/en/contact-us/Pages/bt-contact-form.aspx

Suricata rule for detection:

```
alert http any any -> any any (msg:"Siemens Field Panel Authentication Bypass Using an Alternate Path or Channel, Path Traversal"; http.method; content:"GET"; content:”FieldPanel.xml”; http_uri; reference: cve, CVE-2017-9947; priority:1; sid: 1000001; rev: 1;) 
```

# Scripts:

Two Python scripts are available: siemens_field_panel_scanner.py and APOLOGEE.py. The siemens_field_panel_scanner.py script is a Metasploit module that can be loaded into the framework for simple auxiliary uses on internal Operational Technology and Industrial Control System (ICS) networks. The APOLOGEE.py script is a standalone program for enumerating field panels using standard command line arguments. 

## Install: 

Download repository:

```
$ mkdir APOLOGEE
$ cd APOLOGEE/
$ sudo git clone https://github.com/RoseSecurity/APOLOGEE.git
```

APOLOGEE.py Usage:

```
# python3 APOLOGEE.py <Siemens Field Panel IP>

$ python3 APOLOGEE.py 192.168.1.22
```

siemens_field_panel_scanner.py Usage:

To load the script into Metasploit:

```
# Make the script executable
$ chmod +x siemens_field_panel_scanner.py
# Create directory for module
$ mkdir -p ~/.msf4/modules/auxiliary/scanner/scada
# Move script into folder
$ mv siemens_field_panel_scanner.py ~/.msf4/modules/auxiliary/scanner/scada
```

Fire up Metasploit:

```
$ msfconsole -q
# Reload modules
msf> reload_all
msf> use /modules/auxiliary/scanner/scada/siemens_field_panel_scanner.py
```

If you encounter any errors, check the following log:

```
$ tail ~/.msf4/logs/framework.log
```

If you are interested in writing your own Python modules for Metasploit, check out: https://docs.metasploit.com/docs/development/developing-modules/external-modules/writing-external-python-modules.html
