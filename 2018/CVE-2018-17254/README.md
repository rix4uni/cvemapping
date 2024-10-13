# Joomla-JCK-Editor-6.4.4-SQL-Injection

The JCK Editor Jtreelink plugin for Joomla! fails to correctly parse the user inputs, allowing SQL Injection.
This exploit takes advantage of this security flaw and dump the administrators credentials and possibly upload a PHP RCE shell.

Exploit Title: Joomla JCK Editor 6.4.4 SQL Injection

Google Dork: inurl:/plugins/editors/jckeditor/plugins/jtreelink/

Date: 05/03/2021

Exploit Author: Nicholas Ferreira

Vendor Homepage: http://docs.arkextensions.com/downloads/jck-editor

Version: 6.4.4

Tested on: Debian 10

CVE : CVE-2018-17254

Video explaining the vulnerability, it's exploitation and the code of the exploit (in portuguese): [![](http://img.youtube.com/vi/DqMC0mELPvA/0.jpg)](http://www.youtube.com/watch?v=DqMC0mELPvA "Video")


# Usage
user@lol:~$ php JCKEditor_SQLi_Exploit.php --url target.com/plugins/

You **must** specify the /plugins/ directory. This is because some websites are not hosted on the root of the webserver, e.g, the applications may be as target.com/site/, or target.com/2021/, or something like that. So, by specifying the /plugins/ path, you make sure the vulnerable file will be found.

With -r or --rce, the exploit will try to craft and upload a PHP script that allows remote command execution. This will only work if the MySQL allows stacked queries, which is not enabled in the default configuration, so it will probably not work. =(

With -t or --targets you can specify a list of vulnerable websites, and the exploit will try dump all in sequence.

Sometimes the website administrator can change the default name of the database. In this case, you can get the list of all DBs and manually specify the correct one with -d or --db.

![](https://i.imgur.com/NOrGm2c.png)
