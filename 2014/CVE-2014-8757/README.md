LG On Screen Phone authentication bypass PoC
============================================

What is LG On Screen Phone?
---------------------------
The LG On-Screen Phone application (OSP) makes it easy to access and control LG’s Android smartphones through a PC. The connection can be established either by using an USB cable or wirelessly through Wi-Fi or Bluetooth. When attempting to connect to the phone via OSP, a popup dialog is displayed on the phone and it is to be confirmed and accepted by the owner. Once the channel is established, the screen contents of the device are being transmitted to the PC as a motion stream, mouse clicks on the PC are turned into touch events on the phone. By using OSP one can control an LG Smart Phone just like it was in their hands.

Authentication bypass vulnerability
-----------------------------------
SEARCH-LAB Ltd. discovered a serious security vulnerability in the On Screen Phone protocol used by LG Smart Phones. A malicious attacker is able to bypass the authentication phase of the network communication, and thus establish a connection to the On Screen Phone application without the owner’s knowledge or consent. Once connected, the attacker could have full control over the phone – even without physical access to it. The attacker needs only access to the same local network as the phone is connected to, for example via Wi-Fi.

CVE
---
The ID CVE-2014-8757 was assigned to this vulnerability.

Affected Versions
-----------------
LG On Screen Phone v4.3.009 (inclusive) and older versions of the application are vulnerable.
This vulnerability was fixed in LG OSP v4.3.010

Most smart phone models of LG are affected and the OSP application is even preinstalled, and there is no
option to uninstall or stop it. On newer models, like G3 the OSP application is not preinstalled anymore.

Technical details
-----------------


The vulnerable code resides in the On Screen Phone component:

```
shell@geehrc:/ $ps |grep osp
system    1411  303   559616 44504 ffffffff 00000000 S com.lge.osp
```

It is started automatically on boot and there is no way in the system settings to turn it off.

The process is listening on 0 0.0.0.0:8382:

```
shell@geehrc:/ $ netstat -nap|grep 8382
netstat -nap|grep 8382
 tcp       0      0 0.0.0.0:8382           0.0.0.0:*              LISTEN
```

The LG On Screen Phone client software running on PC connects to this TCP port.
After receiving the initial banner, the client sends the following binary message to the server running on the phone:

```
00000000  18 00 1c 96 dd 82 c2 31  0a 0d 5a dc 05 2a 23 f4 .......1 ..Z..*#.
00000010  21 a5 d3 02 01 00 00 34  33 30 39 30             !......4 3090
```

This message triggers the confirmation dialog on the phone asking the user whether they wanted to allow this connection.
If the user hits cancel, the phone server sends a response with a negative message to the client and then closes the TCP connection immediately.

*However, the server process does not require this message to be sent before serving another requests*, like initiating the video stream or submitting files, handling key/touchscreen events, notifications.
Using a modified client it is possible to connect to the phone without the confirmation dialog being displayed on the phone.

*The attacker has full control over the phone.*


Proof of Concept
----------------
The Proof of Concept code was tested against G1 and G2 models.

This osp-discovery helper script listens for discovery broadcast messages of the official LG On Screen Phone 
application and answers them, so the application would believe a Phone running OSP is available locally.

The osp-proxy script excepts the official LG On Screen Phone application would connect to it,
which is possible by running osp-discovery.pl. 


Timeline
--------
SEARCH-LAB Ltd. responsibly reported this threat to the manufacturer in September 2014 who confirmed the severity of the issue and started working on the fix in turn. The patched version of the application is now available to download through LG’s Update Center and/or will be available in form of Maintenance Release for some models. LG smartphone users should make sure to have at least version 4.3.010 of the On Screen Phone (OSP) application installed. Please note that when OSP is pre-installed, the device is vulnerable by default – OSP is started automatically and cannot be disabled in Settings.

*End Users*: Update the OSP appliaction to revision 4.3.010 or newer through LG Update Center.

Links
-----
https://www.youtube.com/watch?v=Wd8XydalVas
