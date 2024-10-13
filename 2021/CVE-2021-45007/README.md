# CVE-2021-45007

#Cross-Site Request Forgery

Affected product and version: Plesk Obsidian 18.0.37

Severity: High

Impact: Submit requests with attacker information

Description: CSRF could let the attacker to submit new requests because there isn’t any CSRF_token protection sent with requests to server.

Steps to reproduce: 
1.	Login and try to submit any request
2.	Capture the request with burp suite

 ![image](https://user-images.githubusercontent.com/65978029/154807485-fb6ea2d2-0b2c-426f-874b-3972dc4b5326.png)

3.	Will note that there isn’t any token protection sent with request to server
4.	Write simple html exploit to submit request

 ![image](https://user-images.githubusercontent.com/65978029/154807515-e8e23c45-81ca-498c-82c5-e50252ea21ba.png)

5.	Open it in browser

 ![image](https://user-images.githubusercontent.com/65978029/154807530-061d498f-40ee-48db-841c-2c307d52a430.png)

6.	Submit the request

 ![image](https://user-images.githubusercontent.com/65978029/154807542-2bbfee6e-90c9-4fcb-9ee7-9875e4d508a2.png)

7.	Will find that your data are submitted successfully

 ![image](https://user-images.githubusercontent.com/65978029/154807550-41c98ae4-3141-4da0-93a3-4be5af545438.png)








