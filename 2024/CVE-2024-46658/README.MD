
# CVE-2024-46658

Syrotech SY-GOPON-8OLT-L3 v1.6.0_240629 Command Injection Vulnerability

# Usage

1- Edit the URL in the script.

2- Edit the Cookie_Login value in the script.

3- Run the script, it will allow you to executing commands.

# Vulnerability Details

GET /cgi/home.php?fun=system&page=shellCMDExec&isajax=1&runtab=1&cmdExec=1&command=ping%208.8.8.8%20-c%204%0aid&random=1725991418844 HTTP/1.1

Normally, only the ping command is allowed to be executed in the administration panel.

<img src="https://github.com/jackalkarlos/CVE-2024-46658/blob/main/imgs/1.png?raw=true">

If you intercept the request with a proxy, add a new line byte to the end of the command parameter and type the command you want to run, it will allow you to run another command.

<img src="https://github.com/jackalkarlos/CVE-2024-46658/blob/main/imgs/2.png?raw=true">

# Authors

Mehmet Demir

