# CVE-2024-42850
An issue in the password change function of Silverpeas v6.4.2 and lower allows for the bypassing of password complexity requirements.

## Writeup
![Logging in with a single character password](https://github.com/njmbb8/CVE-2024-42850/blob/main/login.PNG?raw=true)

When changing your password, upon submission of the new password, the password is first sent in a POST request to an endpoint which checks to ensure that the password is in compliance with complexity requirements.

![Request to check conformity](https://github.com/njmbb8/CVE-2024-42850/blob/main/password_check.PNG?raw=true)

After Silverpeas has confirmed that the password meets the requirements, a separate POST request is made to update the account with the password with no checks, leading to a possibility of setting a single character password.

![Request to update account](https://github.com/njmbb8/CVE-2024-42850/blob/main/badpw.PNG?raw=true)

![Account update confirmation](https://github.com/njmbb8/CVE-2024-42850/blob/main/confirmation.PNG?raw=true)
