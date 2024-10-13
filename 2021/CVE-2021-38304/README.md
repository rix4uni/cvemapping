# CVE-2021-38304 Proof of Concept
### Overview

This repository contains a proof of concept for a critical security vulnerability in older versions of the National Instruments `nipalk.sys` driver. The vulnerability allows for arbitrary code execution and memory disclosure in kernel mode. It is intended purely for personal research only.

### Description

The `nipalk.sys` driver improperly handles user-supplied pointers during the processing of a specific IOCTL request. This flaw enables an attacker to supply a function pointer that the driver will call in kernel context with controlled parameters.

### Key points

* __Function Pointer Control__: The driver calls a user-supplied function pointer without proper validation.
* __Parameter Control__: The attacker can control the `RCX` and `RDX` registers during the function call.
* __Memory Disclosure__: By calling functions like `RtlCopyMemory`, an attacker can read arbitrary kernel memory.
* __Denial of Service (DoS)__: Passing an invalid function pointer causes a system crash due to the driver's lack of input validation.

### Root Cause

The vulnerability arises from the driver's failure to validate  pointers provided by user-mode applications. During the processing of IOCTL `0xABCD03C4`, the driver retrieves a function pointer from a user-controlled structure and invokes it without proper checks:

```assembly
0045561e 48 8b 01        MOV        RAX,qword ptr [param_1]
00455621 49 8b 52 18     MOV        irp,qword ptr [R10 + 0x18]
00455625 ff 50 08        CALL       qword ptr [RAX + 0x8]
```

* The function pointer at `[RAX + 8]` is executed in kernel context.
* Parameters `RCX` and `RDX` are controlled by the user.

### Output Example

* Successful Memory Leak:

```
[+] Starting exploit
[+] Memory allocated
[+] Values before IOCTL:
   exploit->dummy: 00000000001b0000
   exploit->function_pointer: fffff8017ea21300
[+] Device opened successfully
[+] Sending IOCTL
[+] Values after IOCTL:
   exploit->dummy: 7208f88349c18b48
   exploit->function_pointer: ffff7710f8834937
[+] DeviceIoControl succeeded. Bytes returned: 8
[+] Buffer Output: 1769472
[!] WARNING: exploit->dummy has changed!
[!] WARNING: exploit->function_pointer has changed!
[+] Exploit finished
```

### Disclaimer
This PoC is intended for educational purposes only.
