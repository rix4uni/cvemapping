# CVE-2022-39066

Firmware details:

```
wa_inner_version: BD_POSTEMF286RMODULEV1.0.0B12
cr_version: CR_ITPOSTEMF286RV1.0.0B10
```

## Prerequisites

- requests (`pip install requests`)

## SQL injection

The vulnerability is a SQL injection present in the handler `PHONE_BLOCK_ADD` in the webserver `goahead` binary.

Possible exploits:

- delete any record in any database
- add fake records in any database
- create a file with chosen name in any directory with `rw-` permissions if this file does not exists
- memory dos
- ...

The PoC for this vulnerability is present in this directory, please ensure that syslogs aren't enabled because we need that the file didn't exists. Use the script `poc.py` with the following command:

```bash
$ python3 exploit.py http://<router> <admin_password>
```
 
It shows how an attacker can write a file, in this case I'll write a file in the `/var/log/webshow_messages` (web log) and I'll get the writed file through `cgi-bin/ExportSyslog.sh`

Basically the script use the payload `test'); ATTACH DATABASE '/var/log/webshow_messages' AS t; CREATE TABLE t.pwn (dataz text);INSERT INTO t.pwn (dataz) VALUES ('testestestest');--"`


## Author

- Andrea Maugeri

## References

https://support.zte.com.cn/support/news/LoopholeInfoDetail.aspx?newsId=1027744

