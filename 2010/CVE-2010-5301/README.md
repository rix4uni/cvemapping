# CVE-2010-5301
**A proof of concept of an SEH overflow with arbitrary dll injection**

## Description
Kolibrì HTTP Server 2.0 is affected by a **stack-based buffer overflow**. At the time of discovery this vulnerability was exploited by simply overwriting the instruction pointer with a JMP ESP instruction, where ESP pointed to shellcode dropped on the stack. Subsequently, it was found that the SEH chain could be overwritten if a larger payload was sent. The application does not have valid POP - POP - RET instructions to make the SE handler point to the next SEH record though. This is because all related memory addresses start with a nullbyte.

![nullbytes_seh](https://user-images.githubusercontent.com/98479572/171615000-bf7a3317-d0a2-4d67-a12c-c8eecc578be1.png)

------------------------------------------------------------------------

## The Exploit
This exploit proposes code execution via SEH overflow through DLL injection. Injecting an arbitrary DLL into the Kolibrì process opens up an opportunity for overwriting the SE handler with a nullbyte-free address pointing to a POP - POP - RET instruction from that DLL. Clearly this method can only be used to develop a proof of concept, and cannot be relied on if exploitation is carried out to elevate system privileges locally. This is because you need to have the same privileges of the target process if you want to inject a DLL into it. Other than that, the exploit works!

![poc](https://user-images.githubusercontent.com/98479572/171615533-b94ff1ca-79ef-4ea9-9c9f-b4cb7ca94844.gif)

------------------------------------------------------------------------

## Update
When I first uploaded this exploit it only supported very short custom shellcodes with hardcoded WinExec and ExitProcess addresses. This was due to the short buffer space coming after overwriting the SEH. Now I just updated the exploit code by deploying an egghunter shellcode right after the SEH and dropping the egg + the shellcode in the User-Agent header of the web server. So the execution flow will be redirected from the overwritten SEH to the egghunter, which will then search for the shellcode marked with the egg 'w00t'.

-------------------------------------------------------------------------

## References
Credit for this method goes to FULLSHADE from this original repo.

https://github.com/FULLSHADE/POPPOPRET-nullbyte-bypass

All I have done is applying the idea to this specific CVE.
