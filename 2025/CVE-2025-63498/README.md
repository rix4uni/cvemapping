                                            Stored XSS in cookie Alinto/SOGo 

Researchers: Daniil Khomichenok, Alexander Klimenko

Affected Versions < 5.12.4 ( [https://github.com/Alinto/sogo/releases/tag/SOGo-5.12.4](https://github.com/Alinto/sogo/releases/tag/SOGo-5.12.4#:~:text=attendee%20(736d758)-,login,-%3A%20Only%20remember) )

Date: 01.10.2025

 **********************************************************************************************
 
When the **"Remember Username"** feature is enabled, a base64-encoded field is added to the browser cookie. 

This value is obtained from the **"userName"** parameter in the **POST** request to the **/SOGo/connect** endpoint.

Server response contains b64 encoded XSS payload with set cookie:

**_Set-Cookie:_ SOGoLogin=dGVzdDIyMkBxYXRlc3Qub2YuYnk8L3NjcmlwdD48c2NyaXB0PmFsZXJ0KCcxMjMnKTwvc2NyaXB0Pg%3D%3D; expires=Sun, 02-Nov-2025 09:58:23 GMT;**

Adding the following value to the POST request for the **"userName"** parameter:

<sub> test222@victim.com</script><script>alert('123')</script> </sub>

which contains a **JavaScript injection** that is **_executed_** when the user revisits the authentication page and is stored in the **_"SOGoLogin"_ cookie in the user's browser**.


Code of Auth page, which contains injection:

    <script type="text/javascript">
    var cookieUsername = "test222@victim.com</script><script>alert('123')</script>";
    var language = 'English';
    var loginHint = ''
    </script>

Code of login remember set-cookie which accepts XSS injections as a paramteter value:

    if (rememberLogin)
      [response addCookie: [self _cookieWithUsername: [params objectForKey: @"userName"]]];
      else
      [response addCookie: [self _cookieWithUsername: nil]];


Fix: https://github.com/Alinto/sogo/commit/9e20190fad1a437f7e1307f0adcfe19a8d45184c
