# ScreenConnect-UserEnum

ConnectWise also known as ScreenConnect has a userenum vulnerability. 
This is an user enumeration tool for that

##  CVE-2019-16516
vulnerable <= 19.2.24707 ??? didn't really understand if they fixed in upper version https://docs.connectwise.com/ConnectWise_Control_Documentation/ConnectWise_Control_release_notes/Release_notes_archive#ConnectWise_Control_2019.5

~~~
Tried on verions: 6.4.15787.6556-1472470634
                  6.3.13446.6374-2666439717
~~~

## How To
~~~
usage: screenconnect_userenum.py [-h] [-c cnt] [-v] [-s] [-p proxy] url wordlist

http://example.com/Login user enumeration tool

positional arguments:
  url         http://example.com/Login
  wordlist    username wordlist

optional arguments:
  -h, --help  show this help message and exit
  -c cnt      process (thread) count, default 10, too many processes may cause connection problems
  -v          verbose mode
  -s          stop on first user found
  -p proxy    socks4/5 http/https proxy, ex: socks5://127.0.0.1:9050
~~~


example: python3 screenconnect_userenum.py  -p socks5://127.0.0.1:9050 -v http://example.com/Login user.txt
