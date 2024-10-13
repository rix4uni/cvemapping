# CVE-2019-10207
PoC for CVE-2019-10207 linux kernel: bluetooth: hci_uart: kernel NULL pointer dereference

```
gcc CVE-2019-10207.c -o cve-2019-10207-poc -static
```

test on 4.20.0

kernel compile CONFIG_* must be opened:
```
CONFIG_BT_HCIUART_MRVL=y
CONFIG_BT_MRVL=y
```





