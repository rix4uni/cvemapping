# CVE-2022-3992
Cross-Site Scripting in WonderCMS

Description: A cross-site scripting (XSS) vulnerability in Sanitization Management System v1.0 allows potential attackers to upload arbitrary files via a crafted name into the system logo Fields of the System Info Fields. The cookie has no HttpOnly Flag this could be used to steal the cookies of logged-in users.
How To Reproduce:
<img width="1440" alt="Screen Shot 2022-11-19 at 12 25 34 PM" src="https://user-images.githubusercontent.com/81638590/202848956-49ec4e04-1ade-4ddb-90e3-2a835a764a53.png">
<img width="1403" alt="Screen Shot 2022-11-19 at 12 27 18 PM" src="https://user-images.githubusercontent.com/81638590/202848980-b38c9704-4cd3-462e-8215-4a7364a8c6ba.png">
<img width="1435" alt="Screen Shot 2022-11-19 at 12 31 03 PM" src="https://user-images.githubusercontent.com/81638590/202848992-b14918ba-53d6-43a5-b9c1-3da49069785d.png">
