# Tools for CVE-2018-1000001

## Check vulnerability:
```
$ cat /proc/sys/kernel/unprivileged_userns_clone
```
Output:
```
1
```
If file "/proc/sys/kernel/unprivileged_userns_clone" does not exists:
```
$ unshare -mU /bin/sh -c "sleep 5" & /bin/sh -c "sleep 1; cd /proc/$!/cwd; realpath .; kill -9 $!"
```
The output must contain the string "(unreachable)" before '/':
```
[1] 12345
(unreachable)/home/user
```

## tool.so
Options are passed via Environment variables:
```
TRACE_DEBUG=1  - Value for printing debug information (Default: 0)
STACK_SIZE=100 - Size output data of stack (Default: 100)
```
How to run:
```
$ make
$ cp /bin/umount .
$ LD_PRELOAD="$(realpath tool.so)" TRACE_DEBUG=1 STACK_SIZE=100 ./umount /root
```

## More
https://www.halfdog.net/Security/2017/LibcRealpathBufferUnderflow/
