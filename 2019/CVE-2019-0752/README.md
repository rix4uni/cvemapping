https://www.thezdi.com/blog/2019/5/21/rce-without-native-code-exploitation-of-a-write-what-where-in-internet-explorer

PoC exploit for CVE-2019-0752

Targets Internet Explorer 11 32bit on Windows 10 x64 up to RS4, RS5?

Uses special address values in adddition to some path magic to avoid using powershell and the block comment

Uses javascript to create the necessary dom elements to avoid the use of static html 

No hard coded offsets
