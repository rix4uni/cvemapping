# CVE_POC_test
CVE-2019-13086漏洞的复现以及poc实验代码

原CVE信息：
http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2019-13086

实验环境：
CSZ CMS架构+php5.4+MySQL 5.5+Apache 2.4

漏洞类型：
SQL注入漏洞  文件上传漏洞

简要说明：
在\cszcms\cszcms\core\MY_Security.php的csrf_show_error函数中 
HTTP包的User-Agent字段在被添加到数据库查询语句中之前没有任何内容检测
这成为了可被构造sql注入的地方

防御措施：当然是赶紧修改源码添加对http包的UA字段的检测了！
