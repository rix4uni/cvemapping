# CVE-2023-46870

Nordic Semiconductor nRF Sniffer for Bluetooth LE versions 3.0.0, 3.1.0, 4.0.0, 4.1.0, and 4.1.1 have incorrect file permissions set, which allows adversaries to perform privilege escalation and code execution by modifying bash and python scripts.

**Keywords:** Local Privilege Escalation (LPE), Code Execution

**Affected Platform:** Linux, MacOS

**Affected Files:** extcap/nrf_sniffer_ble.py, extcap/nrf_sniffer_ble.sh, extcap/SnifferAPI/*.py


## Description


nRF Sniffer for Bluetooth LE is a Wireshark extension that allows the use of a nRF52840 dongle and Development Kit to perform packet capture and analysis.


## Replication Steps
1. Download and decompressing the relevant software [nRF Sniffer for Bluetooth LE](https://www.nordicsemi.com/Products/Development-tools/nRF-Sniffer-for-Bluetooth-LE/Download)
2. As described by the vendor in the user manual found at [Installation Guide](https://infocenter.nordicsemi.com/topic/ug_sniffer_ble/UG/sniffer_ble/installing_sniffer_plugin.html), copy the files directly to the Wireshark extcap plug-in folder. Observe the script nrf_sniffer_ble.sh which may have been set to 777, allowing other users in the system to edit the content of the script. 


[YouTube Video](https://youtu.be/cyC4_aJgMX0)
_Video was recorded when got Covid-19, sorry about the slow speaking._

## Analysis
**CVSS:3.0 7.3 High**
Vector: AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H


Due to this permissions issue, the extracted files are set to allow both group and others to modify (permissions set as 777 and 666). This allows any malicious program or user, even without sudo or root permissions, to modify the bash and python scripts, potentially leading to code execution when another user launches Wireshark. Since Wireshark always loads the extensions from the extcap directory, regardless of whether the legitimate user intends to use the "nRF Sniffer for Bluetooth LE" or not, the code will always be executed.


[YouTube Video](https://youtu.be/n6YQiWRjzCY)



## Suggested Mitigation


Manually correct the file permissions to 500 or 400.
For example, on macOS:
```
chmod 500 ~/.config/wireshark/extcap/nrf_sniffer_ble.sh 
chmod 400 ~/.config/wireshark/extcap/SnifferAPI/*
```


## History

- Nov 2, 2023 – CVE ID Reserved.
- Dec 11, 2023 – Vendor Responded, Case concluded invalid.
- May 10, 2024 – Publicly Disclosed.

