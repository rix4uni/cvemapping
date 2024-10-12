# CVE-2023-34845
Vulnerability POC for CVE-2023-34845
### Vulnerability 
I found a cross-site scripting attack on the new content creating page http://localhost:800/admin/new-content
it will execute the script in user context allowing the attacker to access any cookies or sessions tokens retained
by the browser.
Stored XSS, also known as persistent XSS, is the more damaging than non-persistent XSS. It occurs when a malicious script is injected directly into a vulnerable web application.

### Steps to reproduce the problem

- login into the account
- click on the new content like in that image
![new_content](https://user-images.githubusercontent.com/35825039/231964080-750d0578-e861-42f8-8cc6-1776c45192a4.png)

- click on the images button 
![images_button](https://user-images.githubusercontent.com/35825039/231964476-3a66d6d5-4476-42cd-b216-83bdbd0a1493.png)

- select the payload svg file which is injected with xss payload or ssrf payload
![payload](https://user-images.githubusercontent.com/35825039/231965164-0f6c98d5-af2a-4e94-9ccc-9dca63829492.png)


![image-upload_success](https://user-images.githubusercontent.com/35825039/231965296-ccb9eba4-ff4b-461b-87d6-57e86e20a207.png)

- insert and save the page
- copy the image link and open in the new tab 
![popup](https://user-images.githubusercontent.com/35825039/231965564-6c3782f9-b41b-471e-9511-af35b1bc85d3.png)
