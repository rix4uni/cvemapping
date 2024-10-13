# CVE-2018-14699
### UnAuth Command injection in the enable_user function of DroboAccess v2.1
-----
# Usage: 
- To use First startup a listener (ncat -nvlp 1337)
- Next run the exploit

  - example: exploit.py -t 192.168.1.122:8080 -l 192.168.1.2 -p 1337
  
  '-t', '--target', help='host for exploitation, ex. 192.168.1.122:8080',required=True
  
  '-l', '--listener-ip', help='listener IP', required=True
  
  '-p', '--port', help='port number of the listener', required=True

# Description:

CVE-2018-14699 is a blind command injection vulnerability in DroboAccess v2.1. The issue is here because the enable_user function takes the username parameters as user input then calls a dependency that executes a shell directly without any sanatization. I clearify this as there doesn't appear to be another reference of this anywhere. So again this is not a vulnerability in Drobo 5N2 rather a vulnerability in DroboAccess. This has been tested on a B810n with success.

# Details

The script will make an attempt to echo a script to a file called revshell in the current working directly. If this is successful, it will then attempt to call it with bash as the executable, making a connection back to your listener with bash!

# Resources:

- https://blog.securityevaluators.com/call-me-a-doctor-new-vulnerabilities-in-drobo5n2-4f1d885df7fc
- https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-14699
