# CVE-2023-4427

CVE-2023-4427 was found by glazunov, and you can find RCA in his [report](https://bugs.chromium.org/p/project-zero/issues/detail?id=2477)  

chrome version: 117.0.5938.62 in linux from v8ctf.  

I choose a very unstable method. To bypass ASLR, use many iframes with different domains in `main.html` to brute high address, you can change your `/etc/hosts` to implement that locally, if you are a ctfer, you should know it's 1/256 lol, or if ASLR is disabled for debug, you can set bbbase in #L210 to const. Of course there are some more stable methods like use JIT code in area of WASM.  

The exp for v8 is lost, but it's easier than chrome version, understand RCA and you can solve it by yourself.  

More detailed writeup is coming soon(*MAYBE*)  
