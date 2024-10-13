# Description: CVE-2017-8779

rpcbind through 0.2.4, LIBTIRPC through 1.0.1 and 1.0.2-rc through 1.0.2-rc3, and NTIRPC through 1.4.3 do not consider the maximum RPC data size during memory allocation for XDR strings, which allows remote attackers to cause a denial of service (memory consumption with no subsequent free) via a crafted UDP packet to port 111, aka rpcbomb.

CVE link https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-8779

# Installation Procedures
## Assumptions
* The user is familiar with the go programming language
* The user already has a golang development environment configured (Needed to compile)

## Install
### Compile
```
git clone https://github.com/drbothen/GO-RPCBOMB.git
go build RPCBomb.go
```
# Documentation
The compiled RPCBomb.exe has several switches that allows the attacker to tailor the attack as they deem fit.

#### -host
This is a REQUIRED flag. This sets the target system. Defaults to REQUIRED

#### -numbytes
This is NOT a required flag. This sets the number of bytes to try and allocate Defaults to 5999999999

#### -port
This is NOT a required flag. This is the port RPC Bind is running on. Defaults to port 111

#### -loop
This is NOT a required flag. This sets the number of UDP packets to send, or the number of times to request the allocate bytes. Defaults to 1

#### -threads
This is NOT a required flag. This sets the number of child threads to utilize to send UDP packets in concurrence. Defaults to 1
# Credit

Credit belongs to Guido Vranken who originally reported the finding and wrote sample ruby exploit code that this golang exploit is based on located https://github.com/guidovranken/rpcbomb.

The original report can be found at https://guidovranken.wordpress.com/2017/05/03/rpcbomb-remote-rpcbind-denial-of-service-patches/