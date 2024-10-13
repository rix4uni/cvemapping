# CVE-2020-27786 Kernel Exploit
## Details
You can find full details and explaination here: https://1day.dev/notes/Linux-Kernel-n-day-exploit-development

## TL;DR
The vulnerability is a Race Condition that causes a write Use-After-Free. The race window has been extended using the userfaultd technique handling page faults from user-space and using msg_msg to leak a kernel address and I/O vectors to obtain a write primitive. With the write primitive, the modprobe_path global variable has been overwritten and a root shell popped.
