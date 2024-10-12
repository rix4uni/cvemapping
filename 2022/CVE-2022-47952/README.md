> [Suggested description]
> lxc-user-nic in lxc through 5.0.1 is installed setuid root, and may
> allow local users to infer whether any file exists, even within a
> protected directory tree, because "Failed to open" often indicates
> that a file does not exist, whereas "does not refer to a network
> namespace path" often indicates that a file exists. NOTE: this is
> different from CVE-2018-6556 because the CVE-2018-6556 fix design was
> based on the premise that "we will report back to the user that the
> open() failed but the user has no way of knowing why it failed";
> however, in many realistic cases, there are no plausible reasons for
> failing except that the file does not exist.
>
> ------------------------------------------
>
> [Additional Information]
> % ls /l
> ls: cannot open directory '/l': Permission denied
> % /usr/lib/x86_64-linux-gnu/lxc/lxc-user-nic delete lol lol /l/h/tt h h   
> cmd/lxc_user_nic.c: 1096: main: Failed to open "/l/h/tt" <----- file does not exist.
> % /usr/lib/x86_64-linux-gnu/lxc/lxc-user-nic delete lol lol /l/h/t h h
> cmd/lxc_user_nic.c: 1101: main: Path "/l/h/t" does not refer to a network namespace path <---- file exist!
>
> liblxc-common is having a SUID binary that can be abused by a regular
> to know if a file exist or no anywhere in the filesystem, even under
> directories where only the root user can list files.
>
> ------------------------------------------
>
> [Vulnerability Type]
> Insecure Permissions
>
> ------------------------------------------
>
> [Vendor of Product]
> liblxc-common
>
> ------------------------------------------
>
> [Affected Product Code Base]
> liblxc-common - latest 5.0.1
>
> ------------------------------------------
>
> [Affected Component]
> /usr/lib/x86_64-linux-gnu/lxc/lxc-user-nic SUID binary.
>
> ------------------------------------------
>
> [Attack Type]
> Local
>
> ------------------------------------------
>
> [Impact Information Disclosure]
> true
>
> ------------------------------------------
>
> [Attack Vectors]
> To exploit the binary liblxc-common should be installed on the system.
>
> ------------------------------------------
>
> [Discoverer]
> Maher Azzouzi
>
> ------------------------------------------
>
> [Reference]
> https://github.com/lxc/lxc/blob/0b83d71c2c8f3bac9503f894cd84584f79258bb3/lxc.spec.in#L274
> https://github.com/lxc/lxc/blob/0b83d71c2c8f3bac9503f894cd84584f79258bb3/src/lxc/cmd/lxc_user_nic.c#L1085-L1104
> https://bugs.launchpad.net/ubuntu/+source/lxc/+bug/1783591/comments/45

Use CVE-2022-47952.
