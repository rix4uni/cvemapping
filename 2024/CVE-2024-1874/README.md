# CVE-2024-1874
Proof Of Concept for [CVE-2024-1874](https://nvd.nist.gov/vuln/detail/CVE-2024-1874)

### Command Injection via Array-ish $command Parameter of proc_open() (bypass CVE-2024-1874 fix)

***The CVE:*** In PHP versions 8.1.* before 8.1.29, 8.2.* before 8.2.20, 8.3.* before 8.3.8, the fix for CVE-2024-1874 does not work if the command name includes trailing spaces. Original issue: when using proc_open() command with array syntax, due to insufficient escaping, if the arguments of the executed command are controlled by a malicious user, the user can supply arguments that would execute arbitrary commands in Windows shell.

I have created 2 different simple proof of concept exploits for the CVE 2024-1874 in Python and in PHP
