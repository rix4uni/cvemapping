# CVE-2023-49038 Command Injection in Ping Utility on Buffalo LS210D Version 1.78-0.03
Christopher J. Pace and Ryan Miller

The Buffalo LS210D is a Network Attached Storage (NAS) server designed and marketed towards small-businesses and individuals.  Within the LS210D’s admin interface, there exists a built-in ping utility.  This utility uses client-side JavaScript to sanitize input that is directly appended to the system’s ping command.  Unfortunately, server-side filtering is not used, meaning an attacker can inject arbitrary text that will be appended to the name of a host within the ping command.  To exploit this vulnerability, an attacker will need to be an admin of the NAS.

Entering the ping utility, a potential attacker is initially unable to enter special characters, or letters into the “Target IP Address” field.  

![burp](https://github.com/christopher-pace/CVE-2023-49038/assets/22531478/f24c39c2-1d02-4ffa-b096-0218b2b002ef)

In this screenshot, the IP address has been appended with ‘;ping 9.9.9.9’.  On the right side of the screenshot is an SSH session into the NAS running the command ‘watch -n 1 ps -a|grep ping’.  As you can see via this screenshot, arbitrary text can be injected into the NAS’ built-in ping utility.

This is a screenshot of the responsible Perl script, located at /www/buffalo/www/dynamic/system/maint/BufPing.pm, which shows the variable VARIABLE not filtered for arbitrary characters before use in the system ping command.

![code](https://github.com/christopher-pace/CVE-2023-49038/assets/22531478/7e80ef6e-027c-40bc-b664-2e01c9840096)

To resolve this vulnerability, we recommend implementing server-side filtering that matches the filter used for the existing client-side JavaScript.
