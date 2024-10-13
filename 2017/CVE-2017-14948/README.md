# Vulnerabilities in D-Link routers (CVE-2017-14948) 
In this little write-up we will see some bugs I found on D-Link products. D-Link offers a wide range of products, including many different router models, mounting different firmware versions. In this document I will address the following firmware versions: DIR-880L, DIR-868L, DIR-890L, DIR-885L and DIR-895L.
Without any further ado, let's begin.

## Firmware analysis
As I didn't own any of the D-Link routers, and they provide free access to their firmware, I decided to find bugs by only relying on static analysis. Note that, in this section I will refer to the firmware DIR-880L, the other firmware have similar structures.

### DIR-880L
After downloading and unpacking the DIR-880L firmware, I found that its firmware contain a whole squashFS file-system, containing about 2160 files. AS I didn't want to consider each one of them independently, I started looking for the one handling user-inputs.

After analyzing the configuration files and looking for HTTP known headers, I finally restrict my focus on three binaries, and finally on one: fileaccess.cgi.

Here's the disassembly of the vulnerable function:

```c
signed int __fastcall content_type(char *a1)
{
  char *dest; // [sp+4h] [bp-10h]@1
  const char *haystack; // [sp+Ch] [bp-8h]@1
  char *haystacka; // [sp+Ch] [bp-8h]@3

  dest = a1;
  haystack = getenv("CONTENT_TYPE");
  if ( !haystack )
    return -22;
  haystacka = strstr(haystack, "boundary=");
  if ( !haystacka )
    return -22;
  strcpy(dest, haystacka + 9);
  return 0;
}
```
In the above code the content of the variable 'CONTENT_TYPE'  (pointed by the variable haystack) is controlled by a user (through the HTTP request's header). Its content, after the keyword 'boundary', is then copied into a buffer dest, without checking haystacka's length. If one takes a look at the caller function (address 0x1CE6C), one can infer that the size of dest is 256 bytes. As an attacker can control the content of CONTENT_TYPE, she could send the string 'boundary=' followed by as least as 257 characters to trigger a buffer overflow.

Other two similar bugs were found in the same firmware sample, involving the HTTP cookie. 
One of them is shown below:
```c
v10 = getenv("HTTP_COOKIE");
  if ( v10 )
  {
    strcpy((char *)&v5, &v10[v11]);
    v17 = strlen((const char *)&v5);
  }
```
Here, the ariable v10 points to the user cookie, which can be at most 4k bytes (according the RFC2109). However, the variable v5 is as big as 1024 bytes (as we can infer from the function's stack frame). This can trigger a buffer overflow.

These bugs were reported and confirmed by D-Link.


### DIR-868L, DIR-890L, DIR-885L and DIR-895L
These firmware samples present a similar structure as DIR-880L and have the same bugs related to the same HTTP fields.
