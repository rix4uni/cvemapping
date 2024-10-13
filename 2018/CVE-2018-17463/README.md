# CVE-2018-17463
Working Proof of Concept Exploit for CVE-2018-17463 utilzing WebAssembly RWX Pages for Shellcode execution.

CVE-2018-17463 stemmed from the incorrect side effect annotation in V8 in Google Chrome prior to 70.0.3538.64, allowing a remote attacker to execute arbitrary code inside a sandbox via a crafted HTML page.

This Proof of Concept is directly related to the following blog posts:

* [Chrome Browser Exploitation, Part 1: Introduction to V8 and JavaScript Internals](https://jhalon.github.io/chrome-browser-exploitation-1/)
* [Chrome Browser Exploitation, Part 2: Introduction to Ignition, Sparkplug and JIT Compilation via TurboFan](https://jhalon.github.io/chrome-browser-exploitation-2/)
* [Chrome Browser Exploitation, Part 3: Analyzing and Exploiting CVE-2018-17463](https://jhalon.github.io/chrome-browser-exploitation-3/)

The original writeup for this bug was presented in [Phrack: Exploiting Logic Bugs in JavaScript JIT Engines](http://phrack.org/issues/70/9.html#article) by [Samuel Gross](https://twitter.com/5aelo?lang=en). 

All credits to finding the bug and writing the initial proof of concept go to Samuel Gross.
