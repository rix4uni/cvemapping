# CVE-2018-14772

### info

This is a PoC Remote Code Execution exploit for CVE-2018-14772, a vulnerability 
that I discovered in the [pydio](https://pydio.com/) file sharing platform. It 
requires pydio application administrator credentials to work. You can run the 
exploit like so:

### usage

```
$ python exploit.py -h
usage: exploit.py [-h] -t TARGET -u USERNAME -p PASSWORD -L LISTENER_IP -P
                  LISTENER_PORT [--payload PAYLOAD]

[*] exploit some pydio boxes (academically)

optional arguments:
  -h, --help         show this help message and exit
  --payload PAYLOAD  one of the pre-built reverse-shell payloads (1, 2, 3, 4,
                     or 5), or a custom command. keep in mind you can't use
                     the (") character as it breaks the injection

required arguments:
  -t TARGET          this is the target URI for the pydio instance..i.e.
                     http://127.0.0.1:31337/pydio/
  -u USERNAME        this is the username of the admin user
  -p PASSWORD        this is the password of the admin user
  -L LISTENER_IP     IP address to catch reverse shell on
  -P LISTENER_PORT   port to catch reverse shell on
```

I baked in a few reverse shell payloads you can try. Additionally, you can use ad-hoc custom shell commands. Keep in mind, using the `"` character will break the command injection, so you have to work around that limitation.

### example exploitation

![img](https://i.imgur.com/oBXqt78.png)

### writeup

found on my blog [here](http://coastalsec.io/cve-2018-14772-remote-code-execution)
