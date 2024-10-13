CVE-2021-3656:

This issue is caused by missing validation of the the `virt_ext` VMCB
field and allows a malicious L1 guest to disable both VMLOAD/VMSAVE
intercepts and VLS (Virtual VMLOAD/VMSAVE) for the L2 guest. Under
these circumstances, the L2 guest is able to run VMLOAD/VMSAVE
unintercepted, and thus read/write portions of the host physical
memory.


Setup Environment to access Linux Kernel:
1. You could use a Docker container or use a Virtual Machine. I will do my best with a
docker container

2. You want to have Docker Desktop setup on MAC or Windows. If you have a Linux
machine by default, you can ignore all these steps.

3. Next you want to pull an ubuntu image from:[ ubuntu - Official Image | Docker Hub](https://hub.docker.com/_/ubuntu/)

a. For Windows you can type “docker pull ubuntu” in PowerShell or CMD

b. Same for MAC
i. Note: This will pull the latest version of ubuntu. You may want to pull an
older version so you could have a older version of its kernel
ii. Create a directory with a Dockerfile in it. The file at bare minimum needs
to have: “From ubuntu:16.04”
iii. To get an older version type: “docker build -t ubuntu-xenial” for example
iv. To check your current images type: “docker image ls”

c. Once you run the command from iii, the system will provide you with a container
ID.
i. You can check “docker container ls” to make sure the container is
available

d. Moving up to access this container you are going to want to type: “docker exec -it
<NAMES> <COMMAND>”

e. You should now be in your container in the directory “/”

f. This exploit was found in kernel version 4.13; we need to make sure that is the
version that our workplace is running
i. To check type: uname -r

g. From here you find the kernel directory by typing: “cd sys/kernel”

h. From here I did not make much progress since I could not find a way to
downgrade to kernel 4.13

i. I also tried downgrading using virtual machines, but that did not work
either


REFERENCES:

● oss-security - [[CVE-2021-3653, CVE-2021-3656] SVM nested virtualization issues in
KVM (openwall.com)](https://www.openwall.com/lists/oss-security/2021/08/16/1)
○ This is an overview of two vulnerabilities that were found in the KVM’s AMD code
for supported nested virtualization

● This is the PATCH: [kvm/kvm.git - kernel-based virtual machine - kvm](https://git.kernel.org/pub/scm/virt/kvm/kvm.git/commit/?id=c7dfa4009965a9b2d7b329ee970eb8da0d32f0bc)

● KVM: SVM: [Enable Virtual VMLOAD VMSAVE feature · torvalds/linux@89c8a49
(github.com)](https://github.com/torvalds/linux/commit/89c8a4984fc9)
○ This is the vulnerable code

● [RHSA-2021:3676 - Security Advisory - Red Hat Customer Portal](https://access.redhat.com/errata/RHSA-2021:3676)

● [CVE-2021-3656- Red Hat Customer Portal](https://access.redhat.com/security/cve/cve-2021-3656)
○ Red Hat description of the exploit

●[ 1983988 – (CVE-2021-3656) CVE-2021-3656 kernel: SVM nested virtualization issue in](https://bugzilla.redhat.com/show_bug.cgi?id=1983988)
KVM (VMLOAD/VMSAVE) (redhat.com)

● [What is KVM? (redhat.com)](https://www.redhat.com/en/topics/virtualization/what-is-KVM)
○ Explanation on what a KVM is

● [How to Check Linux Kernel Version in Command Line (4 Easy Options)
(phoenixnap.com)](https://phoenixnap.com/kb/check-linux-kernel-version#:~:text=The%20hostnamectl%20command%20is%20typically%20used%20to%20display,The%20second-to-last%20line%20should%20read%3A%20Kernel%3A%20Linux%203.10.0-957.21.2.el7.x86_64.)

● How to downgrade the Linux Kernel articles/videos

○ [How to Downgrade the Kernel in Linux - Make Tech Easier](https://www.maketecheasier.com/downgrade-kernel-linux/#:~:text=1%20Boot%20Into%20an%20Older%20Kernel.%20The%20good,type%20of%20problem%20is%20to%20avoid...%20More%20)
○ [How to Downgrade from WSL Version 2 to WSL Version 1 - MSSQL DBA Blog
(peter-whyte.com)](https://peter-whyte.com/how-to-downgrade-from-wsl-2-to-wsl-1/#:~:text=How%20to%20Downgrade%20from%20WSL%202%20to%20WSL,other%20post%20%E2%80%93%20How%20to%20Check%20WSL%20Version)
○ [Linux Series - 2.1.5 Upgrading/Downgrading the Linux Kernel - YouTube](https://www.youtube.com/watch?v=rcM8gDwjAkw&t=2s)

● [How to check KVM is installed in Ubuntu Linux - Linux Shout (how2shout.com)](https://www.how2shout.com/linux/how-to-check-kvm-is-installed-in-ubuntu-linux/)
○ Need to have KVM for this exploit

● [How to install QEMU/KVM on Ubuntu 22.04 | 20.04 LTS - Linux Shout (how2shout.com)](https://www.how2shout.com/linux/how-to-install-qemu-kvm-on-ubuntu-22-04-20-04-lts/)

● [How To Install Linux Kernel 4.13 In Ubuntu And Linux Mint? (fossbytes.com)](https://fossbytes.com/install-linux-kernel-4-13-ubuntu-linux-mint/#:~:text=At%20the%20top%2C%20you%20can%20see%20Linux%20kernel,reboot%20your%20computer%20and%20use%20the%20new%20kernel.)
○ How to install the Linux Kernel 4.13
