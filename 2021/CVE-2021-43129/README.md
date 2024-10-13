# [CVE-2021-43129](https://nvd.nist.gov/vuln/detail/CVE-2021-43129)
## Vulnerability in D2L Brightspace’s Learning Management System(LMS) 
### Vulnerability Type:
>[CWE-668: Exposure of Resource to Wrong Sphere](https://cwe.mitre.org/data/definitions/668.html)
### Vendor of Product:
>Desire2Learn/D2L
### Affected Product Code Base:
>D2L Brightspace’s Learning Management System(LMS) 
>>Tested version: 20.21.7

#### [D2L announced that the  "Disable Right Click" setting will be retired in August 2022.](https://community.brightspace.com/s/article/retirement-notice-disable-right-click)

### Affected Component:
>Quizzing's "Disable Right Click" setting
### Attack Type:
>Remote
### Impact Escalation of Privileges:
>True
### Attack Vectors:
>The remote quiz taker can remove "&ispriv=&drc=1" from the quiz URL, reload, and have full privilege to highlight text, copy and paste via keyboard controls, and print the test data via keyboard controls.
# Methodology and Description
While taking quizzes with the setting "Disable right click" enabled, I found it can disabled by removing data from the GET request. The "Disable Right Click" setting is used to prevent users from having the privilege to highlight text, copy and paste via keyboard controls, and print the test data via keyboard controls. An exploit can remove the "Disable Right Click" setting completely for a remote user taking the quiz.
# Proof of Concept
After starting a quiz with the "Disable right click" setting enabled, the users search bar will contain this highlighted data.
![1](https://github.com/Skotizo/CVE-2021-43129/blob/main/example/1.png)
The quizzes "Disable right click" setting acts as intended in its current state. When using CRTL+P results in this popup message.

![2](https://github.com/Skotizo/CVE-2021-43129/blob/main/example/2.png)

If the quiz taker to remove "&ispriv=&drc=1" and reloads the page, the user now has the priviledge to highlight text, copy and paste via keyboard controls, and print the test data via keyboard controls.
![3](https://github.com/Skotizo/CVE-2021-43129/blob/main/example/3.png)

The ou and qi elements GET request data were removed because they are personally identifying and does not effect the vulnerability. I disclosed this vulnerability privately and gave time to remediate in order to strengthen the integrity of the D2L's LMS application. 
***
## Simplified POC

The request to load the quiz with the "Disable Right click" function enabled.

`https://domain.com/d2l/lms/quizzing/user/attempt/quiz_start_frame_auto.d2l?ou=123456&isprv=&drc=1&qi=123456&cfql=0&dnb=0&fromQB=0`

The request to load the quiz and disable the "Disable Right click" setting.

`https://domain.com/d2l/lms/quizzing/user/attempt/quiz_start_frame_auto.d2l?ou=123456&qi=123456&cfql=0&dnb=0&fromQB=0`

# Timeline 
* Initial disclosure to D2L - 08/10/2021

* D2L acknowledged the vulnerability - 08/11/2021

* Payment recieved for disclosure of vulnerability - 09/10/2021

* CVE ID request - 10/27/2021

* D2L announced "Disable Right click" retirement in August, 2022 - 02/15/2022

* CVE-2021-43129 assigned - 3/30/2022

* Public Disclosure - 4/15/2022

* CVE description updated - 4/19/2022

* Issued request to change CVE-2021-43129 discription based upon D2L suggestion - 4/20/2022

* NIST updated the webpage with the CWE and CWSS

