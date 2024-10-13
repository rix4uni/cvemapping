# ctl_ctloutput-leak

<!-- Brandon Azad -->

The `ctl_ctloutput` function in macOS High Sierra 10.13 ignores the return value of a call to
`sooptcopyin`, which opens up a race window to leak uninitialized kernel heap data to user space.
ctl_ctloutput-leak is a proof-of-concept exploit that attempts to trigger this information leak.
Exploitation requires root privileges.

This exploit has been confirmed to work on macOS High Sierra 10.13.1 Beta 17B25c and iOS 10.1.1
14B100 (under mach_portal).

## The vulnerability: CVE-2017-13868

Here is the relevant part of `ctl_ctloutput` on [macOS High Sierra 10.13][ctl_ctloutput source]:

[ctl_ctloutput source]: https://opensource.apple.com/source/xnu/xnu-4570.1.46/bsd/kern/kern_control.c.auto.html

```c
if (sopt->sopt_valsize && sopt->sopt_val) {
	MALLOC(data, void *, sopt->sopt_valsize, M_TEMP,	// (a) data is allocated
		M_WAITOK);					//     without M_ZERO.
	if (data == NULL)
		return (ENOMEM);
	/*
	 * 4108337 - copy user data in case the
	 * kernel control needs it
	 */
	error = sooptcopyin(sopt, data,				// (b) sooptcopyin() is
		sopt->sopt_valsize, sopt->sopt_valsize);	//     called to fill the
}								//     buffer; the return
len = sopt->sopt_valsize;					//     value is ignored.
socket_unlock(so, 0);
error = (*kctl->getopt)(kctl->kctlref, kcb->unit,		// (c) The getsockopt()
		kcb->userdata, sopt->sopt_name,			//     implementation is
			data, &len);				//     called to process
if (data != NULL && len > sopt->sopt_valsize)			//     the buffer.
	panic_plain("ctl_ctloutput: ctl %s returned "
		"len (%lu) > sopt_valsize (%lu)\n",
			kcb->kctl->name, len,
			sopt->sopt_valsize);
socket_lock(so, 0);
if (error == 0) {
	if (data != NULL)
		error = sooptcopyout(sopt, data, len);		// (d) If (c) succeeded,
	else							//     then the data buffer
		sopt->sopt_valsize = len;			//     is copied out to
}								//     userspace.
```

This code does the following:
1. It allocates a kernel heap buffer for the data parameter to `getsockopt`, without specifying the
   `M_ZERO` flag to zero out the allocated bytes.
2. It copies in the `getsockopt` data from userspace using `sooptcopyin`, filling the data buffer
   just allocated. This copyin is supposed to completely overwrite the allocated data, which is why
   the `M_ZERO` flag was not needed. However, the return value of `sooptcopyin` is not checked,
   which means it is possible that the copyin has failed, leaving uninitialized data in the buffer.
   The copyin could fail if, for example, the program passed an unmapped address to `getsockopt`.
3. The code then calls the real `getsockopt` implementation for this kernel control socket. This
   implementation should process the input buffer, possibly modifying it and shortening it, and
   return a result code. However, the implementation is free to assume that the supplied buffer has
   already been initialized (since theoretically it comes from user space), and hence several
   implementations don't modify the buffer at all. The NECP function
   [`necp_ctl_getopt`][necp_ctl_getopt source], for example, just returns 0 without processing the
   data buffer at all.
4. Finally, if the real `getsockopt` implementation doesn't return an error, `ctl_ctloutput` calls
   `sooptcopyout` to copy the data buffer back to user space.

[necp_ctl_getopt source]: https://opensource.apple.com/source/xnu/xnu-4570.1.46/bsd/net/necp.c.auto.html

Thus, by specifying an unmapped data address to `getsockopt`, we can cause a heap buffer of a
controlled size to be allocated, prevent the contents of that buffer from being initialized, and
then reach a call to `sooptcopyout` that tries to write that buffer back to the unmapped address.
All we need to do for the copyout to succeed is remap that address between the calls to
`sooptcopyin` and `sooptcopyout`. If we can do that, then we will leak uninitialized kernel heap
data to userspace.

It turns out that this is a pretty easy race to win. While testing on my 2015 Macbook Pro, the mean
number of attempts to win the race was never more than 600, and the median was never more than 5.
On iOS 10.1.1 on an iPhone 7 the race was even easier to win, typically taking no more than 2
attempts. (This testing was conducted with `DEBUG` off, since the printfs dramatically slow down
the exploit.)

## Usage

To build, run `make`. See the top of the Makefile for various build options.

Run the exploit by specifying the target leak size on the command line:

	$ sudo ./ctl_ctloutput-leak 128
	000000:  ef be ad de ef be ad de  00 00 00 00 00 00 00 00
	000010:  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00
	000020:  00 00 00 00 00 00 00 00  01 00 00 00 40 80 00 00
	000030:  de 28 45 00 04 00 00 00  a0 ff 4a 26 80 ff ff ff
	000040:  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00
	000050:  08 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00
	000060:  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00
	000070:  00 00 00 00 00 00 00 00  ef be ad de ef be ad de

## Timeline

I reported this issue to Apple on October 7, 2017. It was assigned CVE-2017-13868. Apple fixed the
issues in [macOS 10.13.2] and [iOS 11.2].

[macOS 10.13.2]: https://support.apple.com/en-us/HT208331
[iOS 11.2]: https://support.apple.com/en-us/HT208334

## License

The ctl_ctloutput-leak code is released into the public domain. As a courtesy I ask that if you
reference or use any of this code you attribute it to me.
