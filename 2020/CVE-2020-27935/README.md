# SnatchBox

SnatchBox (CVE-2020-27935) is a sandbox escape vulnerability affecting macOS up to version 10.15, as well as early beta versions of macOS 11.0. The most significant impact of SnatchBox is that it allows a malicious publisher to escape the non-optional macOS App Store sandbox and obtain complete access to all of the user's files, breaking the security model of the App Store on macOS.

## The Vulnerability
The fact that in macOS, in contrast to iOS for example, a userspace task voluntarily puts itself into a sandbox is vulnerable by design. Since this is a task a potentially malicious author has almost full control of its memory mappings and contents, and code that runs prior to sandbox initialization (e.g. dyld itself, or the Objective-C runtime) parses the contents of this potentially malicious binary, carefully crafted data can be used for gaining code execution before sandbox initialization. If the process would never execute any code, including dyld code, before being enforced into a sandbox, this wouldn't have been a problem, as early code execution would not gain anything for the attack in that case. It is conceptually similar to [Saagar Jha's sandbox bypass](https://saagarjha.com/blog/2020/05/20/mac-app-store-sandbox-escape/), except it bypasses the newly introduced mitigations and App Store validations.

## Exploitation before 10.15

Before macOS 10.15 exploitation of this bug is fairly simple. One would create a binary that contains an Objective-C category for a class that is used prior to sandbox initialization (Such as `OS_xpc_object`) and override a method (preferably an inherited one to avoid runtime warnings) that is used prior to sandbox initialization (Such as `+initialize`, which is implicitly called on the first access to a class). Because categories are loaded before sandbox initialization, and the first access to `OS_xpc_object` (or other suitable victim classes) is done after loading categories and before sandbox initialization, the attacker provided `+initialize` method (Or another suitable victim method) will be called prior to sandbox initialization, allowing one to access data outside the container, for example. Alternatively, the attacker can replace reference to `_libsecinit_initializer` (Which initializes the sandbox) with nop-like function to (potentially conditionally) disable the sandbox even after resuming execution.

## Exploitation in 10.15 and 11.0 beta

The Objective-C runtime used in macOS 10.15 is not vulnerable to the exploitation technique previously detailed, because categories are not loaded before `didCallDyldNotifyRegister` is set, making our `+initialize` method to be called only after sandbox initialization happens.

However, `map_images` is still called on our binary, making it possible to alter runtime data in unintended ways that would allow us to execute code before sandbox initialization. The complete, commented exploitation is in main.c, but I will go through the basic details here. We craft an Objective-C class structure whose `data` pointer points to a location in `libxbc.dylib`. That location must be chosen in a way that `flags` will have bit 31 (`RW_REALIZED`) set, so the runtime will not attempt to realize this invalid class and crash, and `firstSubclass` must share its address with the `isa` of a class we want to override. Another (meta) class will inherit from this invalid class, and provide its own `+initialize` method. We add the subclass to `__objc_nlclslist` so the runtime realizes this class.

When the runtime realizes our subclass, which happens before sandbox initialization, it will call `addSubclass` on our invalid superclass and subclass, which will replace the victim's `isa` with a pointer to our subclass, effectively replacing all its methods with our `+initialize`. When our `+initialize` method is called, which will be prior to sandbox initialization if we chose a proper victim class, we can again replace `_libsecinit_initializer` references with nops (Conditionally or not), and fix runtime changes we have done to resume execution without crashing later on.

## Provided Demo

The provided demo can be built by running `make`, creating a file at `~/Documents/SecretDocument.txt`, and running `SnatchBox.app/Contents/MacOS/SnatchBox` from the terminal (A bundle is created because it is required by `com.apple.security.app-sandbox`, but this is still a command line program). The built binary is signed with `com.apple.security.app-sandbox` which would normally prevent access to `~/Documents/SecretDocument.txt` (As it is not in our container), but will be able to read its data anyway. Due to runtime structure changes this demo will not work on macOS 10.14 and earlier unmodified, but will work on 10.15 and 11.0 (Tested: 10.15.4, 10.15.7 and 11.0 Beta (20A5354i)). The two exploitation techniques can be combined to target both runtime versions, but such demonstration is not provided.

Example run:
```
CatalinaVM:SnatchBox lior$ make
mkdir -p SnatchBox.app/Contents/MacOS/
clang -O3 -Wall -framework Foundation main.m -o SnatchBox.app/Contents/MacOS/SnatchBox
cp Info.plist SnatchBox.app/Contents/
codesign --force --sign - SnatchBox.app --entitlements ent.xml
CatalinaVM:SnatchBox lior$ echo "Quack"> ~/Documents/SecretDocument.txt
CatalinaVM:SnatchBox lior$ codesign -d --entitlements :- SnatchBox.app/Contents/MacOS/SnatchBox 
Executable=/Volumes/SharedFolders/Home/Projects/SnatchBox/SnatchBox.app/Contents/MacOS/SnatchBox
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>com.apple.security.app-sandbox</key>
    <true/>
    <key>com.apple.security.files.user-selected.read-only</key>
    <true/>
</dict>
</plist>
CatalinaVM:SnatchBox lior$ SnatchBox.app/Contents/MacOS/SnatchBox 
Found libsecinit_initializer at 0x7fff72309124
Found libSystem.B.dylib at 0x7fff6f0de000
Found __DATA at 0x7fff984eeca0
Replacing libsecinit_initializer reference at 0x7fff984eed48 with a nop
2020-12-18 16:31:48.196 SnatchBox[804:8043] Attempting to read protected file: /Users/lior/Documents/SecretDocument.txt
2020-12-18 16:31:48.197 SnatchBox[804:8043] Escaped sandbox! The contents are: <51756163 6b0a>
```

## Impact

As previously mentioned, this allows creating a macOS App Store application that does not run in a sandbox despite being required to do so by the App Store policy. The vulnerability can also be used in a framework, which can be used by otherwise legitimate App Store applications. Lastly, it can even be combined with something similar to "Xcode Ghost" to mass-inject malicious code that runs outside the sandbox to App Store applications.

## Fix

Apple fixed the exploit during the beta testing stage of macOS 11.0 by adding a call to `malloc_size` in `realizeClassWithoutSwift`. This confirms that if a class is marked as realized (`RW_REALIZED`, like our fake class), it indeed has a valid, *malloc'ed* data pointer, with the correct size (0x20 bytes). If this is not the case, the runtime will abort with a message similar to `realized class 0x100002078 has corrupt data pointer 0x7fff88c00948`. The fix was also applied to iOS, iPadOS, tvOS and watchOS; even if not directly affected.