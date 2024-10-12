# CVE-2023-51073 - Firmware Update Server Verification Vulnerability on Buffalo LS210D Version 1.78-0.03


Christopher J. Pace and Ryan Miller

The Buffalo LS210D is a Network Attached Storage (NAS) server designed and marketed towards small-businesses and individuals.  Within the LS210D is the ability to remotely download and install a firmware update.  The LS210D is vulnerable to an “Adversary in the Middle”, or AitM, attack within this feature.  An attacker controlling the upstream connection of a victim will be able to either provide an incorrect DNS name for the update server, or redirect the traffic from the update server to a malicious server.  This can lead to command execution as the root user, or direct installation of malware.

The file /etc/init.d/update_notifications.sh is called from the firmware upgrade server-side script at /www/buffalo/www/dynamic/system/update/BufUpdate.pm.  Inside of update_notifications.sh is the following line:

![firmware-source](https://github.com/christopher-pace/CVE-2023-51073/assets/22531478/dbb3a903-93c1-43fc-a89d-d31522810ab8)


Opening this xml file reveals that the XML file itself also points to an HTTP-only connection:

![xml-file](https://github.com/christopher-pace/CVE-2023-51073/assets/22531478/656fdaea-d3f6-4050-b59f-e22ed5391c06)


Further, this zip file is also not encrypted.  Previous research into this model pointed us towards downloading a manual firmware update utility, which did include a password-protected zip file.  The file linkstation_series_1.75-0.01.zip does not contain these protections.  Within the archive is the file hddrootfs.buffalo.updated, which contains the archive hddrootfs.buffalo, which contains the root filesystem for the LS120D.  An attacker can directly view and modify this zip file to include their own malware or read sensitive files.

![firnware-shadow](https://github.com/christopher-pace/CVE-2023-51073/assets/22531478/2fd07f5c-7c15-4e9b-a9a7-88717d83ad70)


Once an attacker has performed an AitM attack, the router will happily offer to install the updated firmware.  Here is an example of such an attack, with the screen on the right showing the necessary modifications to fw_info2.xml, namely adding 0x0000001D to the productId tag, and incrementing the version type tag to a version greater than the victim’s firmware version (1.78-0.04 in this case).

![firmware-update-available](https://github.com/christopher-pace/CVE-2023-51073/assets/22531478/2eba26ea-90ee-4bcf-a4eb-f37920a3312d)

![recommendations](https://github.com/christopher-pace/CVE-2023-51073/assets/22531478/af317267-bc56-479b-b0dd-15b39f906379)
