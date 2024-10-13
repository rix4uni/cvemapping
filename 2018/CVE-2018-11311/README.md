# mySCADA myPRO 7 Hardcoded Credentials
# CVE-2018-11311

https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-11311

https://www.exploit-db.com/exploits/44656/

http://myscada.org/wp-content/uploads/downloads/BOXv7/changelog.txt

```
Changelog v7.0.46
-----------------
- fix of possible vulnerability as described here https://vuldb.com/?id.118038
  - This release disables download of project using FTP protocol. The download is performed over secure SSL channel now. 
  - You don't have to do anything to activate this, it is done automatically. After the installation restart your system TWICE please. 
- minor bug fixes - speed optimisation  
```


# I. Background
myPRO is a professional HMI/SCADA system designed primarily for the visualisation and control of industrial processes. myPRO is effective and innovative solution for any industry that needs to be under non-stop operation. myPRO guarantees reliable supervision, a userfriendly interface and superior security.
It supports Windows OS (32/64-bit), Mac OS X and Linux (32/64-bit) platforms.
(more: https://www.myscada.org/mypro/)

# II. Problem Description
In the latest version of myPRO (v7), it has been discovered that the ftp server's -running on port 2121- username and password information is kept in the file by using reverse engineering. Anyone who connects to an FTP server with an authorized account can upload or download files onto the server running myPRO software.

# III. Technical
Firstly, I found that what ports myPRO listened to. You can get information used by the netstat command about the ports and the services running on it. As you can see from the pictures, when you install myPRO, you can see many ports open. The vulnerability works on all supported platforms.

## (username:password) = (myscada:Vikuk63)

![alt tag](https://emreovunc.com/images/mySCADA_myPRO/open-ports.png)

![alt tag](https://emreovunc.com/images/mySCADA_myPRO/netstat-1.png)

![alt tag](https://emreovunc.com/images/mySCADA_myPRO/netstat-2.png)

In my first research on the Windows OS, myPRO has many process and I noticed that ‘myscadagate.exe’ is listening to port #2121. The 2121 port is important because it could be an ftp service.

![alt tag](https://emreovunc.com/images/mySCADA_myPRO/windows-processes.png)

![alt tag](https://emreovunc.com/images/mySCADA_myPRO/port-2121.png)

As you can see from the picture below, I found that they put the username and password (myscada:Vikuk63) in the source code. I obtained access by connecting to port 2121 of myPRO's server with any FTP client.

![alt tag](https://emreovunc.com/images/mySCADA_myPRO/username&password.png)

![alt tag](https://emreovunc.com/images/mySCADA_myPRO/file-upload-2.png)

![alt tag](https://emreovunc.com/images/mySCADA_myPRO/file-upload.png)

# IV. Solution
As a workaround you need to restrict port 2121 access from the outside. There is no permanent solution for the vendor because there is no patch available.
