Test for [CVE-2021-3864](https://access.redhat.com/security/cve/CVE-2021-3864).

How to run
----------

* create a user
* `echo <username> ALL= path/to/gen-core >> /etc/sudoers`
* `sysctl kernel.core_pattern=core`
* ./cve-2021-3864
* It should generate a core file in /etc/logrotate.d
