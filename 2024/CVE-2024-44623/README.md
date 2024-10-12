# CVE-2024-44623
In [SPX-GC](https://github.com/TuomoKu/SPX-GC) 1.3.0v and below versions, user-controlled input was passed in the exec function of the child_process module without any sanitization, leading to unauthenticated blind remote code execution.

## Vulnerability
In [/routes/routes-api.js](https://github.com/TuomoKu/SPX-GC/blob/65f284f4b9dad4e8c694dd9de0086238c4f7d2b9/routes/routes-api.js#L37-L39), user input received from file param and passed into exec function of child_process leads to unauthenticated blind RCE

## Blind RCE
Blind Remote Code Execution (RCE) in web applications occurs when an attacker can execute arbitrary code on a server without immediate feedback or direct knowledge of the results. This vulnerability often arises from improper user input handling and can be exploited through mechanisms like command execution. 
References:
* OWASP Foundation's [OWASP Cheat Sheet Series: Command Injection](https://cheatsheetseries.owasp.org/cheatsheets/OS_Command_Injection_Defense_Cheat_Sheet.html)
* [CWE-94](https://cwe.mitre.org/data/definitions/94.html): Improper Control of Generation of Code ('Code Injection')

## Affected Product
[SPX-GC](https://github.com/TuomoKu/SPX-GC) <= 1.3.0v

## Fixed Version
Fixed in [31c96893a193428a3a11499ed0e165125f9bbe23](https://github.com/TuomoKu/SPX-GC/commit/31c96893a193428a3a11499ed0e165125f9bbe23) commit, 
The changes were added to the master branch, so the new build and installation from that branch are not vulnerable. The fix has not yet been published as a release on GitHub.


## CVE ID
CVE-2024-44623

## Vulnerability Type
Blind Remote Code Execution

## Root Cause
Usage of user input at `require('child_process').exec('open "' + folder + '"');` function in the [routes/routes-api.js](https://github.com/TuomoKu/SPX-GC/blob/65f284f4b9dad4e8c694dd9de0086238c4f7d2b9/routes/routes-api.js#L37-L39) file

## Impact
Shell commands can be executed by an unauthenticated user in the instances where the vulnerable [SPX-GC](https://github.com/TuomoKu/SPX-GC) tool is running.

## CVSS
[9.8](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H)

## References
Vulnerable Code: [routes/routes-api.js#L37-L39](https://github.com/TuomoKu/SPX-GC/blob/65f284f4b9dad4e8c694dd9de0086238c4f7d2b9/routes/routes-api.js#L37-L39)

Fix Commit: [31c96893a193428a3a11499ed0e165125f9bbe23](https://github.com/TuomoKu/SPX-GC/commit/31c96893a193428a3a11499ed0e165125f9bbe23#diff-771d4a46cb6eface108cd4b3c49a3469f7ec37754eef4552eb65586159cbdcddR42-R47)
