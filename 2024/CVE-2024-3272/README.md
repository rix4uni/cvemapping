# Dinkleberry 🫐

Are you one of the 92,000+ people<sup>1</sup> stuck with a D-Link NAS vulnerable to CVE-2024-3272, and no patch in sight?

This tool uses the exploit itself to patch a vulnerable device.

<sup>1</sup>: See original disclosure in refs

## What it does

Dinkleberry will execute a command to swap out the vulnerable `nas_sharing.cgi` file with a patched version - overwriting the `system()` call with [NOP](https://en.wikipedia.org/wiki/NOP_(code))s.

The `/usr/local/modules` folder (where the file lives) is read-only, so instead a copy is created in `/usr/local/config`, and the symlink in `/var/www/cgi-bin` is updated to point to the safe(r) version.

I have chosen to only NOP the system call so that the command still responds as usual, just without actually executing anything.

>[!NOTE]
> The filesystem is re-loaded from flash on boot. Applying this patch will only work until you reboot the device.
> If you want a more permanent fix, you'll have to re-flash the firmware - perhaps with [Debian](https://github.com/ggirou/dns320)

## Usage

```console
aliask:~/git/dinkleberry$ python3 ./src/main.py -h                                                                                                                   10:01:02
usage: dinkleberry [-h] [--telnet] [--kill-telnet] [--test] [--verbose] target

positional arguments:
  target         Target NAS to patch

options:
  -h, --help     show this help message and exit
  --telnet       Start telnet server
  --kill-telnet  Stop telnet server
  --test         Test if device is vulnerable
  --verbose, -v  Set this to print debug messages
```

If no optional flags are applied, the script performs the patching.

### Telnet

If you just want to poke around on the device, use the `--telnet` command, which starts a telnet session on port 23.

This is hilariously insecure, but your device is already hilariously insecure so may as well take the convenient shell.

## Disclaimer

>[!CAUTION]
> Use this tool at your own peril. It's modifying the actual device software. 
> 
> I am not responsible for:
> - Your device stopping working
> - Losing data stored on the NAS
> - Starting a fire
> - The TA who was happily exploiting this your device being upset

## Final Words

During [analysis](./docs/decompiled-funcs.md) of the `nas_sharing.cgi` and `libsmbif.so` binaries, it quickly became clear that the software on this device is _extremely_ vulnerable. Unmaintainable-rewrite-from-scratch vulnerable.

There are like 80 calls to `system()` in `nas_sharing.cgi` alone - many of these have a pathway for user input. I haven't bothered analysing them all to look for more holes to patch, but here's one S-tier example:

```c
/*  Why use system() instead of libc fopen/fwrite?
    What if you want to write a long string or your filename is long?
    Painfully obvious command injection playground 🤦 */
void append_to_file(const char* string, const char* file) {
  char s_cmd[1024];
  sprintf(s_cmd, "echo %s >> %s", string, file);
  system(s_cmd);
  return;
}
```

Besides all these _insane_ `system` calls, there are more buffer overflows than you can poke a stick at - and I can poke a lot of sticks.

This CVE is on CISA's [KEV list](https://cisa.gov/known-exploited-vulnerabilities-catalog) - **If you have one of these things on the internet, take it offline. Like now.**

Maybe even take D-Link's advice and replace the EOL device. But I wouldn't buy a D-Link product that's for sure.

## References

- Original disclosure: https://github.com/netsecfish/dlink
- NVD page: https://nvd.nist.gov/vuln/detail/CVE-2024-3272
