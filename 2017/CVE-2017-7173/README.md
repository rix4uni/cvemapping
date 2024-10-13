# sysctl_coalition_get_pid_list-dos

<!-- Brandon Azad -->

The `sysctl_coalition_get_pid_list` function in `bsd/kern/sys_coalition.c` uses the
`coalition_get_pid_list` function to collect a list of PIDs in a coalition. This function will
return the number of PIDs if successful or a negative errno on failure. However, the
`sysctl_coalition_get_pid_list` function does not properly check for the error condition, meaning
it will try to send a negative number of PIDs to userspace via `SYSCTL_OUT`. Since the length
parameter is a `size_t`, the result is a call to copyout with a very large value.

I at first thought that this would be a kernel information leak, since the kernel would try to
copy from the stack into a userspace buffer but eventually reach an unmapped page and abort the
copy. However, `SYSCTL_OUT` does not copy out partial values, and on macOS copyio aborts early if
the address plus size wraps around. This makes this bug not exploitable on macOS.

However, on iOS (or at least on iOS 10.1.1) the copyio function triggers a panic if the address
plus size wraps around. This means that this bug can be used for denial-of-service.

Exploitation requires root privileges.

## Timeline

I reported this issue to Apple on September 21, 2017. It was assigned ~~CVE-2017-13833~~
CVE-2017-7173. Apple fixed the issues in [macOS 10.13.2] and [iOS 11.2].

[macOS 10.13.2]: https://support.apple.com/en-us/HT208331
[iOS 11.2]: https://support.apple.com/en-us/HT208334

(Apple has since discovered that CVE-2017-13833 was previously assigned to a different issue and
reassigned this issue CVE-2017-7173.)

## License

The sysctl_coalition_get_pid_list-dos code is released into the public domain. As a courtesy I ask
that if you reference or use any of this code you attribute it to me.
