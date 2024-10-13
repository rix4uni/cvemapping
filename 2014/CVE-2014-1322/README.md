# IPC-Memory-Mac-OSX-Exploit
IPC Local Security Bypass

Inter Process Communication through shared memory is a concept where two or more process can access the common memory. And communication is done via this shared memory where changes made by one process can be viewed by another process.

The kernel in Apple OS X through 10.9.2 places a kernel pointer into an XNU object data structure accessible from user space, which makes it easier for local users to bypass the ASLR protection mechanism by reading an unspecified attribute of the object.

# Details
https://nvd.nist.gov/vuln/detail/CVE-2014-1322
