# CVE-2013-3651 PoC - EC-CUBE 2

## Using

### Require

- Python 3

### Exec

```
$ python poc_cve_2013_3651.py <Target URL>

- e.g.
$ python poc_cve_2013_3651.py http://127.0.0.1:9000/
Result: Vulnerable!
```

## PoC

- 脆弱性 | ECサイト構築・リニューアルは「ECオープンプラットフォームEC-CUBE」  
https://www.ec-cube.net/info/weakness/weakness.php?id=49

## Reference

- JVNDB-2013-000062 - JVN iPedia  
https://jvndb.jvn.jp/en/contents/2013/JVNDB-2013-000062.html

- ECサイト構築で多く利用されている「EC-CUBE」を用いたウェブサイトでの情報漏えい被害の増加について：IPA 独立行政法人 情報処理推進機構  
https://www.ipa.go.jp/security/announce/alert20191225.html
