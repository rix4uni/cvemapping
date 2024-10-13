# NETIS router (WF2419) RCE (CVE-2019-19356)

# Context

The vulnerability is an authenticated Remote Code Execution (RCE) as root through the NETIS (WF2419) router Web management page.

The vulnerability has been found on firmware version V1.2.31805 and on the last available firmware version V2.2.36123. Other models and firmware may also be vulnerable.

# Prerequisites

In order to exploit the vulnerability, a few prerequisites are required. Indeed, we need to reach the router Web management page. Moreover, if an authentication is enforced, we would need to authenticate by trying weak/default password, by performing Man-In-The-Middle attacks, or using any other mean.

# Vulnerability details

Once authenticated, we can notice the "System Tools" menu, which has a "Diagnostic Tools" link. The "Diagnostic Tools" allows performing UNIX "ping" and "tracert" system commands. The IP Address or the Domain Name could be specified in the form. The operating system would then run the chosen command on the specified IP Address and display the command output on the web page.

On the "ping" command, a filter in place prevents performing executing other commands than the “ping” command. It was not possible to bypass that filter.
However, in the "tracert" command, it was possible to perform OS command execution by using the “|” operator.

# Exploit
`python netis_rce.py http://192.168.1.1 "ls"`
