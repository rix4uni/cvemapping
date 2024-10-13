# CVE-2014-0094

検証用。

<https://piyolog.hatenadiary.jp/entry/20140417/1397750197> を参考に、

- vulhub/java:7u55-jdk
- tomcat-8.0.5
- struts-2.3.16

を再現。classLoaderは動いてるけど、肝心のログがパーセントエンコードされちゃってるのでRCEまでつながらない ><

---

windowsバージョンも追加(7u191だけど・・・)。  
これもだめなので、tomcatが原因かな・・？
