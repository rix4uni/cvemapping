# CVE-2020-24227
Playground Sessions - Storing User Credentials in Plaintext

Playground Sessions v2.5.582 (and earlier) for Windows, stores the user credentials in plain text allowing anyone with access to C:\Users\<USER>\AppData\Roaming\Playground\Local Store\#SharedObjects\Playground.swf\UserProfiles.sol to extract the email and password.

Login Page:<br><br>
![alt text](https://github.com/nathunandwani/CVE-2020-24227/blob/main/login-page.jpg?raw=true)

Password:<br><br>
![alt text](https://github.com/nathunandwani/CVE-2020-24227/blob/main/password.jpg?raw=true)

<br><br>Disclosure Timeline:<br>
*August 18, 2020 - Reported to info@playgroundsessions.com - Gave 90 day disclosure timeline - No response
*November 21, 2020 - Public Disclosure