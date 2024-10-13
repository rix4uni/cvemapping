CVE-2007-2447
====

CVE-2007-2447 - Samba usermap script.
</br>
https://amriunix.com/post/cve-2007-2447-samba-usermap-script/

## Usage:
```shell
$ python usermap_script.py <RHOST> <RPORT> <LHOST> <LPORT>
```
  * `RHOST` -- The target address
  * `RPORT` -- The target port (TCP : 139)
  * `LHOST` -- The listen address
  * `LPORT` -- The listen port

## Installation

    sudo apt install python python-pip
    pip install --user pysmb
    git clone https://github.com/amriunix/CVE-2007-2447.git

### Disclaimer:

All the code provided on this repository is for educational/research purposes only. Any actions and/or activities related to the material contained within this repository is solely your responsibility. The misuse of the code in this repository can result in criminal charges brought against the persons in question. Author will not be held responsible in the event any criminal charges be brought against any individuals misusing the code in this repository to break the law.
