# Notes to defend against this exploit
* Patching
  * Just do it... now.
  * Subscribe to/watch the [Pi-hole repository](https://github.com/pi-hole/pi-hole) for new releases (and Issues and Pull requests if you're serious).
* Network
  * Do not expose Pi-hole to the internet.
  * Only expose Pi-hole DNS port 53 to DNS clients, not other ports like management interface.
* Management
  * Use unique and complex (meaning many characters) passphrases for admin account.

# CVE-2020-8816
**The full PoC is available in the PDF document**

This is a variation of a PoC for RCE on Pi-hole 4.3.2: https://natedotred.wordpress.com/2020/03/28/cve-2020-8816-pi-hole-remote-code-execution/ 

The original PoC requires the **$PATH** variable to be 'opt/pihole:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'. This is not the case for a Pi-hole installation on Ubuntu Server with default settings.

Therefore, my PoC requires the **$PWD** variable for www-data to be '/var/www/html/admin'. This should be the case for more types of Pi-hole installations. My PoC also solves a problem: this new string from **$PWD** does not contain the letter ‘p’ required for a ‘php -r' execution as used in the original PoC.
