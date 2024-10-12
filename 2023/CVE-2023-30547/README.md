## CVE-2023-30547
PoC Exploit for VM2 Sandbox Escape Vulnerability

![alt img](https://rvizx.github.io/CVE-2023-30547.png?raw=true)

### Description
vm2 < 3.9.17 is vulnerable to arbitrary code execution due to a flaw in exception sanitization. Attackers can exploit this by triggering an unsanitized host exception within `handleException()`, enabling them to escape the sandbox and run arbitrary code in the host context.

## VM2-Exploit
⚠️ Consider using the "**[VM2-Exploit](https://github.com/rvizx/VM2-Exploit)**" tool, which can be used to exploit **all versions** of VM2, and it's easy to use.

### Indenfity whether the target is vulnerable

run this on the sandbox to find whether the target is vulnerable or not.

```js
const version = require("vm2/package.json").version;

if (version < "3.9.17") {
    console.log("vulnerable!");
} else {
    console.log("not vulnerable");
}
```

## Usage

```
git clone https://github.com/rvizx/CVE-2023-30547
cd CVE-2023-30547
python3 exploit.py
```

or 

```
wget https://raw.githubusercontent.com/rvizx/CVE-2023-30547/main/exploit.py
python3 exploit.py
```

## Credits

### PoC and Analysis
https://gist.github.com/leesh3288/381b230b04936dd4d74aaf90cc8bb244

### Credits
[Xion](https://twitter.com/0x10n) (SeungHyun Lee) of [KAIST Hacking Lab](https://kaist-hacking.github.io/)