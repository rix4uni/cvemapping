# CVE-2019-17026 - A Firefox JIT bug

- Original bug caught in the wild by [Qihoo 360](https://blogs.360.cn/post/apt-c-06_0day.html).
- Exploit written by [maxpl0it](https://twitter.com/maxpl0it).
- Works on Firefox < 72.0.1

This is an exploit for CVE-2190-17026:
*IonMonkey type confusion with StoreElementHole and FallibleStoreElement*

This exploit does not use a sandbox escape, so for testing the *security.sandbox.content.level* attribute in *about:config* needs to be set to 0. It should be possible to chain this with [CVE-2020-0674](https://github.com/maxpl0it/CVE-2020-0674-Exploit) via [PAC](https://googleprojectzero.blogspot.com/2017/12/apacolypse-now-exploiting-windows-10-in_18.html) to get a sandbox escape on Windows.

The writeup for this vulnerability and the steps taken to exploit it can be found [here.](https://labs.f-secure.com/blog/exploiting-cve-2019-17026-a-firefox-jit-bug/)

