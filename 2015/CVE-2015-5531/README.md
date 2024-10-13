# CVE-2015-5531-POC

# 漏洞背景
Elasticsearch是荷兰Elasticsearch公司的一套基于Lucene构建的开源分布式RESTful搜索引擎，它主要用于云计算中，并支持通过HTTP使用JSON进行数据索引。 Elasticsearch 1.6.1之前版本中存在目录遍历漏洞。远程攻击者可借助快照的API调用利用该漏洞读取任意文件。

# 使用说明
```
-u 指定URL
-f 指定读取的文件
```
此POC基于网上现有的进行了魔改，将获取的结果自动进行了Unicode解码，代码较粗糙

<img width="360" alt="image" src="https://user-images.githubusercontent.com/62680449/191476115-82cfc74f-b1e4-4834-be33-02992569e825.png">
