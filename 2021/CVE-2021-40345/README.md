# NagiosXI RCE File-Upload
CVE-2021-40345

Authentified RFI to RCE Nagios/NagiosXI exploitation

Step 1 : 
Go on the "dashlets" managing page and download one of them (I'm using "rss_dashlet" for the exemple) : 
```
http://TARGET_IP/nagiosxi/admin/dashlets.php?download=rss_dashlet
```

Step 2 : 
Modify the *.inc.php (I'm gonna use a tiny PHP reverse shell oneliner in line 34 for the exemple) :

![nagios1](https://user-images.githubusercontent.com/61753065/120605130-ffea4080-c44d-11eb-9dd6-bfba1ae56403.png)

Step 3 : 
Start your listener and upload the malicious dashlet in the dashlets managing page :

![nagios2](https://user-images.githubusercontent.com/61753065/120605611-8e5ec200-c44e-11eb-9111-40ee68ac35d8.png)

And voilà, you got the shell ! 
