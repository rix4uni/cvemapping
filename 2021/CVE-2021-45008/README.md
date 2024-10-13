# CVE-2021-45008

Privilege Escalation from user to admin


Affected product and version: Plesk Obsidian 18.0.37


Severity: Critical


Impact: Gain high privilege from user to admin and access critical information


Description: insecure permissions vulnerability that allows unprivilege user to get admin rights.



Steps to reproduce:

1.	Login with user account with low roles
2.	Capture the request with burp

![image](https://user-images.githubusercontent.com/65978029/154923387-398f42ea-a159-4bd1-b53e-59de6b0e6ee5.png)

3.	Will note that the Super admin flag parameter is false
4.	Forward the request to login
 
 ![image](https://user-images.githubusercontent.com/65978029/154923422-2b022a02-9562-4edc-8844-fab6a4607241.png)


5.	Now logout and enter credentials to login again and capture the request
6.	Change the value of Super admin flag parameter from false to true and forward the request
![image](https://user-images.githubusercontent.com/65978029/154923463-a5b6479e-635b-496f-9c9e-5dc5555d49b1.png)

7.	Will see more information like bank account and other info
 
![image](https://user-images.githubusercontent.com/65978029/154923523-34823f79-7fd0-47dc-8d91-70a88f12464b.png)
