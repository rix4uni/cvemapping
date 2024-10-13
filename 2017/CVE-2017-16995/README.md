# 漏洞描述
Ubuntu是一个以桌面应用为主的开源GNU/Linux操作系统，基于Debian GNU/Linux 。近期有白帽子爆出 ubuntu 的最新版本（Ubuntu 16.04）存在本地提权漏洞，漏洞编号为CVE-2017-16995。该漏洞存在于调用eBPF bpf(2)的Linux内核系统中，当用户提供恶意BPF程序使eBPF验证器模块产生计算错误，导致任意内存读写问题， 低权限用户可使用此漏洞获得管理权限。
该漏洞在老版本中已经得到修复，然而最新版本中仍然可被利用，官方暂未发布相关补丁，漏洞处于0day状态。

# 影响版本
Linux Kernel Version 4.14-4.4
仅影响Ubuntu/Debian发行版本

# 漏洞等级
 高危
# 演示
~~~
bearcat@ubuntu:/opt$ lsb_release -a
<br>No LSB modules are available.
<br>Distributor ID: Ubuntu
<br>Description:    Ubuntu 16.04.4 LTS
<br>Release:        16.04
<br>Codename:       xenial
<br>bearcat@ubuntu:/opt$ uname -a
<br>Linux ubuntu 4.4.0-116-generic #140-Ubuntu SMP Mon Feb 12 21:23:04 UTC 2018 x86_64 x86_64 x86_64 GNU/Linux
<br>bearcat@ubuntu:/opt$ id
<br>uid=1000(bearcat) gid=1000(bearcat) <br>groups=1000(bearcat),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),110(lxd),115(lpadmin),116(sambashare)
<br>bearcat@ubuntu:/opt$ ls
<br>exploit.c
<br>bearcat@ubuntu:/opt$ gcc exploit.c -o exploit
<br>bearcat@ubuntu:/opt$ ./exploit
<br>task_struct = ffff88003a0db800
<br>uidptr = ffff8800374b76c4
<br>spawning root shell
<br>root@ubuntu:/opt# id
<br>uid=0(root) gid=0(root) groups=0(root),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),110(lxd),115(lpadmin),116(sambashare),1000(bearcat)
<br>root@ubuntu:/opt#
~~~

# 漏洞修复
#### 方法一：
目前暂未有明确的补丁升级方案提出，但是建议用户通过修改内核参数限制普通用户使用bpf(2)系统调用来缓解：
设置参数“kernel.unprivileged_bpf_disabled = 1”通过限制对bpf(2)调用了访问来防止这种特权升级<br>
 `root@Ubuntu# echo 1 > /proc/sys/kernel/unprivileged_bpf_disabled`<br>
 #### 方法二：
 升级Linux Kernel 版本，需要重启服务器之后生效：
这一步在环境搭建过程中已经描述过了具体的操作，用户只需要修改内核版本即可！<br>
 #### 方法三：
 代码补丁 https://github.com/torvalds/linux/commit/95a762e2c8c942780948091f8f2a4f32fce1ac6f
 
