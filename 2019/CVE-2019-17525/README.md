# CVE-2019-17525

**D-LINK ROUTER "MODEL NO: DIR-615" with "FIRMWARE VERSION:20.10" &amp; "HARDWARE VERSION:T1**

A vulnerability found on login-in page of D-LINK ROUTER "DIR-615" with "FIRMWARE VERSION:20.10" & "HARDWARE VERSION:T1" which allows attackers to easily bypass CAPTCHA on login page by BRUTEFORCING.

**TARGET**

"Log-in page" of D-LINK ROUTER "MODEL NO: DIR-615" with "FIRMWARE VERSION:20.10" & "HARDWARE VERSION:T1"(IP Address of router login).

**ATTACK SCENARIO AND REPRODUCTION STEPS**

1. Find the PUBLIC IP of the TARGET NETWORK.
2. On browsing the Target IP in the browser, we will get a ROUTER LoginPage.
3. Fill the required login credentials.
4. Fill the CAPTCH properly and Intercept the request in Burpsuit.
5. Send the Request to Intruder and select the target variables i.e. username & password which will we bruteforce under Positions Tab
6. Set the payloads on target variables i.e. username & password under Payloads Tab.
7. Set errors in (the validatecode is invalid & username or password error, try again) GREP-MATCH under Options Tab.
8. Now hit the start attack and you will find the correct credentials.

**REGARDS**

Huzaifa Hussain

https://twitter.com/disguised_noob

https://www.linkedin.com/in/huzaifa-hussain-046791179
