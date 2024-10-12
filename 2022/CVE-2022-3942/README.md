# CVE-2022-3942

Cross Site Scripting in Sanitization Management System

Description: A cross-site scripting (XSS) vulnerability in Sanitization Management System v1.0 allows potential attackers to execute arbitrary web scripts or HTML via a crafted payload injected into the Remarks or Address Fields of the Request Quote Form. As soon as the logged-in staff or admin user opens the quote the XSS is triggered - coupled with the fact that the cookie has no HttpOnly Flag this could be used to steal cookies of logged-in users.


How to Reproduce:
<img width="1092" alt="XSS_CVE_2022-3942" src="https://user-images.githubusercontent.com/20245897/201322144-e0e4736b-dce6-48d9-bea7-6db3b2f4d5f5.png">

<img width="358" alt="Form submission" src="https://user-images.githubusercontent.com/20245897/201322343-40c7471b-2ab5-426d-8e82-af5ef1142d8e.png">
<img width="1184" alt="request opened" src="https://user-images.githubusercontent.com/20245897/201322462-863ac592-b2bd-44ec-aba3-4bcca81acf23.png">
<img width="820" alt="cookies stolen" src="https://user-images.githubusercontent.com/20245897/201322505-a5995abc-91c8-4855-874b-1786af0b869e.png">
