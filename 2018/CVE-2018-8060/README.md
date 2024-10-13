# SIOCtl
## Simple IOCTL dispatcher
<br>
This is a generic IOCTL "dispatcher". I made this to be used as a POC for CVE 2018-8060 and 2018-8061, but it can be used to any device, IOCTL and data, thought. 

* Input data is a binary file, containing raw data to be used as input buffer in IO control.
* Output data is displayed as hexdecimal dump.


## CVE 2018-8060 
* Description: <br>
HWiNFO AMD64 Kernel driver version 8.98 and lower allows unprivileged user to send IOCTL to device driver. If input and/or output buffer pointers are null or if these buffer's data are invalid a null/invalid pointer occurs, resulting into Windows kernel panic a.k.a Blue Screen. 
<br>

* POC: <br>
An unprivileged user sends some IOCTLs, to symbolic device "HWiNFO32", higher than 0x85FE2600 with in/out buffer's data being arbitrary, results in a pointer dereference inside the scope of the device driver; causing a kernel panic. Some cases results into CWE-476 (NULL Pointer Dereference) or CWE-781 (Improper Address Validation in IOCTL with METHOD_NEITHER I/O Control Code)
   - The easiest way to trigger it, is to use input buffer as null :).
 
 
## CVE 2018-8061 
* Description: <br>
HWiNFO AMD64 Kernel driver version 8.98 and lower allows unprivileged user to send special IOCTL to device driver, resulting in direct physical memory read or write. <br>

* POC: <br>
An unprivileged user sending an especial IOCTLs, i.e 0x85FE2608 to symbolic device "HWiNFO32", with in-buffer (user-space) containing a physical memory address, size and a virtual memory address, results in the driver mapping the physical memory and reading it, copying its content to the virtual address.<br> 
The file 8061.data is formatted in this fashion:
   - Phy. Address: FFFFF7F100002000 (source)
   - Size: 00000008        
   - Dest. Virt. Address: 4141414141414141



