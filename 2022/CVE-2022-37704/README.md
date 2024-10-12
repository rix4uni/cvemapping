> [Suggested description]
> Amanda 3.5.1 has a flaw that allows privilege escalation from the
> regular user backup to root. The SUID binary located at
> /lib/amanda/rundump will execute /usr/sbin/dump as root with controlled
> arguments from the attacker which may lead to escalation of privileges,
> denial of service, and information disclosure.
>
> ------------------------------------------
>
> [Additional Information]
> Amanda is a well known software and the package is present on all known Linux distributions and even on Windows.
> I think this bug is critical for that specific software, I may say this a trust vulnerability (the rundump binary trust /usr/sbin/dump) but unfortunately dump can be tampered with to have root shell.
> I will upload a PoC video when sending the e-mail!
>
> ------------------------------------------
>
> [VulnerabilityType Other]
> External software flaw
>
> ------------------------------------------
>
> [Vendor of Product]
> Amanda
>
> ------------------------------------------
>
> [Affected Product Code Base]
> rundump - 3.5.1
>
> ------------------------------------------
>
> [Affected Component]
> The affected component is rundump SUID binary from Amanda software.
> The affected C file is : rundump.c
> The affected line of code is :     execve(dump_program, argv, env);
>
> ------------------------------------------
>
> [Attack Type]
> Local
>
> ------------------------------------------
>
> [Impact Denial of Service]
> true
>
> ------------------------------------------
>
> [Impact Escalation of Privileges]
> true
>
> ------------------------------------------
>
> [Impact Information Disclosure]
> true
>
> ------------------------------------------
>
> [Attack Vectors]
> This vulnerability is an LPE to root.
> To exploit the flaw and become root the attacker should execute a bash script.
>
> ------------------------------------------
>
> [Reference]
> http://www.amanda.org/
>
> ------------------------------------------
>
> [Discoverer]
> Maher Azzouzi

Use CVE-2022-37704.
