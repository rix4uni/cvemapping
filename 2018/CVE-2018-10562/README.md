# PINGPON EXPLOIT

* Author: [@037](https://twitter.com/037)

Pingpon is a tool used to obtain thousands of vulnerable GPON home routers using Shodan.io to then execute any Linux command on using a remote code execution flaw (CVE-2018-10562). 

## DISCLAIMER

I am NOT responsible for any damages caused or any crimes committed by using this tool. 

Original Script: [github.com/f3d0x0/GPON](https://github.com/f3d0x0/GPON)

### Prerequisites

You're required to install Python 3.x

```
apt-get install python3
```

You also require to have the Shodan and Request modules installed
```
pip install shodan
```
```
pip install requests
```


### Using Shodan API

This tool requires you to own an upgraded Shodan API

You may obtain one for free in [Shodan](https://shodan.io/) if you sign up using a .edu email

![alt text](https://raw.githubusercontent.com/649/Pingpon-Exploit/master/1.png)
![alt text](https://raw.githubusercontent.com/649/Pingpon-Exploit/master/2.png)

