# UsbRt SMM Privilege Elevation

This is a Proof-of-Concept code that demonstrates the exploitation of the CVE-2017-5721 vulnerability. This PoC causes a system to be completely stuck because of Machine Check Exception occurred. 

All you need is [CHIPSEC Framework](https://github.com/chipsec/chipsec) installed. And don't forget to put `GRUB_CMDLINE_LINUX_DEFAULT="quiet splash acpi=off"` in `/etc/default/grub` if you have Intel device.  

Usage example:  
```
sudo python poc.py
```
