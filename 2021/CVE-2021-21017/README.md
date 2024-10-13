# CVE-2021-21017

## Not another Adobe Reader Byte Order Mark bug :)

```
# IA32 plugin, ver. 2020.013.20074.
char * __cdecl FUN_2581894c(char *base_url,LPCSTR rel_url)
{
  ............................................................
  ............................................................
  if ((base_url != (char *)0x0) && (rel_url != (LPCSTR)0x0)) {
    if ((*base_url == -2) && (base_url[1] == -1)) {
      iVar6 = bytes_len(base_url);
      pcVar7 = base_url + iVar6;
      pcVar8 = rel_url + 2;
      do {
        do {
          cVar3 = *pcVar8;
          pcVar1 = pcVar8 + 2;
          *pcVar7 = cVar3;
          pcVar2 = pcVar7 + 2;
          cVar4 = pcVar8[1];
          pcVar7[1] = cVar4;
          pcVar7 = pcVar2;
          pcVar8 = pcVar1;
        } while (cVar3 != '\0');
      } while (cVar4 != '\0');
    }
    else {
      lstrcatA(base_url,rel_url);
    }
    return base_url;
  }
  .............................................................
  .............................................................
}
```

When building an absolute URL from one relative to a PDF document's `baseURL` to be used by APIs like: `app.launchURL`, `document.submitForm` or `app.media.createPlayer`,
if the the `baseURL` looks to be a `UTF-16BE` string, the relative one is also treated as a `UTF-16BE` string when performing the concatenation, though it is actually an ANSI string.

This may result in Out-of-bounds read access on one hand. On the other hand, when allocating memory to hold the destination buffer, the relative URL is "measured" as an ANSI string. This is of course not enough if OOB read occurs. (string + the `NULL` terminator filling a whole heap chunk).

What does this mean?

## Type confusion => Out of bounds read => Heap overflow => FULL BUKAKE!

## Poc Attached

It will most often result in a crash and occasionally in overwriting an ArrayBuffer's `byteLength` to `0xFF`.

If you have questions feel free to contact me on twitter: https://twitter.com/Zeusb0x

## Detection

The PDF document catalog will have an `URI` entry holding an indirect reference to a dictionary object. This in turn will have a `Base` entry, which is the actual `baseURL`. It will be most likely be present in hexadecimal notation and will start with the characters `\xFE\xFF`. (see PoC). Fortunately this is the only way to change a documents's `baseURL` in a normal, non-privileged context. Trying to do it from `JavaScript` will throw a security exception.

