# CVE-2022-1015
A write-up and Local Privilege Escalation Proof-of-Concept of an OOB read and write vulnerability in the Linux Kernel.

You can find the [write-up](https://ysanatomic.github.io/cve-2022-1015/) of this vulnerability on my [blog](https://ysanatomic.github.io/) and you can find my introduction to `nf_tables` [here](https://ysanatomic.github.io/netfilter_nf_tables/) as well.

### An Important note
The exploit provided in this repository should not be expected to run successfully on vulnerable kernel versions out of the box.
There are many offsets that would differ between kernel builds as well as of course differing ROP gadgets.

Sometimes even the way the vulnerability is exploited might have to be changed due to differences between kernel builds. An example is another write-up of this vulnerability by David Bouman (@pqlqpql) that you can find [here](https://blog.dbouman.nl/2022/04/02/How-The-Tables-Have-Turned-CVE-2022-1015-1016/#4-cve-2022-1015) where he exploits the vulnerability using *UDP packets* - targetting the stack when a UDP packet is being handled - which couldn't have been done on my kernel build due to significant differences in the stack layout. Instead I used a method targetting the stack when a *TCP ACK* packet is being handled.

If you have the desire to test it out on your end I would recommend reading my write-up and follow the path of finding out the offsets, what hooks to use, etc.

The exact kernel version from which I built the kernel that I was targetting in the write-up was `5.12.0`, commit `9f4ad9e425a1d3b6a34617b8ea226d56a119a717`.

### Building the exploit
To build the exploit you need the libraries `libmnl` and `libnftnl` as well as the POSIX thread (pthread) library.
Building it then is as simple as 
```
gcc -lmnl -lnftnl -lpthread exploit.c -o exploit
```

### Vulnerable versions
The vulnerability arises from `nft_validate_register_store` introduced in commit `345023b0db315648ccc3c1a36aee88304a8b4d91` in version `5.12` and is patched in commit `6e1acfa387b9ff82cfc7db8cc3b6959221a95851` in version `5.17`.

### Legal Disclaimer
This Proof-of-Concept and the write-up of the vulnerability are for **educational purposes only**.
I am not legally responsible for any way this code might get used.
