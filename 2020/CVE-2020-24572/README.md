# CVE-2020-24572-POC
An issue was discovered in includes/webconsole.php in RaspAP 2.5. With authenticated access, an attacker can use a misconfigured (and virtually unrestricted) web console to attack the underlying OS running this software, and execute commands on the system including ones for uploading of files and execution of code.
This is a remake of https://github.com/lb0x/cve-2020-24572.
If you wish to use the original click on their link.

I added payload options, and didn't limit the exploit to the hopes of having sudo rights on executing /etc/raspap/lighttpd/configport.sh
I think anyone can do sudo -l and exploit it incase it's there.
Like always this is for education purposes only.
