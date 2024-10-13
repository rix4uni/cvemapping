# cve-2022-19052

`[mod_alias]` security: potential path traversal with specific configs  
Security: potential path traversal of a single directory above the alias  
target with a specific mod_alias config where the alias which is matched  
does not end in `/`, but alias target filesystem path does end in `/`.

```
e.g. server.docroot = "/srv/www/host/HOSTNAME/docroot"
     alias.url = ( "/img" => "/srv/www/hosts/HOSTNAME/images/" )
```

If a malicious URL "/img../" were passed, the request would be  
for directory "/srv/www/hosts/HOSTNAME/images/../" which would resolve  
to "/srv/www/hosts/HOSTNAME/".  If mod_dirlisting were enabled, which  
is not the default, this would result in listing the contents of the  
directory above the alias.  An attacker might also try to directly  
access files anywhere under that path, which is one level above the  
intended aliased path.

## CVE credit: 
```
Orange Tsai(@orange_8361) from DEVCORE
Script by 1vere$k
```

## Usage 

```
1. git clone https://github.com/iveresk/cve-2018-19052.git
2. cd cve-2018-19052
3. chmod +x cve-2018-19052.sh
4. ./cve-2018-19052.sh -t <IP> or ./cve-2018-19052.sh -f <File_Name>
```

## Contact
You are free to contact me via [Keybase](https://keybase.io/1veresk) for any details. 