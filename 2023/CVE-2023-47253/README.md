# CVE-2023-47253
CVE-2023-47253 | Qualitor &lt;= 8.20 RCE

## Description
Qualitor is a platform for business process management, and this system is present in various companies in Brazil that can be identified simply by using Google dorking.

Our team identified a vulnerability in the application susceptible to Remote Code Execution (RCE), which allows remote execution of PHP code, such as functions like system() and passthru().

In the code below, you can see the source code of the vulnerable page calling an eval() function, which enables the remote execution of codes. This occurs in the file /html/ad/adpesquisasql/request/processVariavel.php.

```php
include("../../../../configLingua.php");
header("Content-type: text/javascript; charset=".$_SESSION['A_appEncoding']);
header("Expires: Thu, 01 Jan 1990 00:00:00 GMT");

$strReturn = '';

eval($_REQUEST['gridValoresPopHidden']);

importClass('AdPesquisaSqlVar');
$bean = new AdPesquisaSqlVarBean();

$vo = $bean->povoaVoComArray($_REQUEST);

if (in_array($_REQUEST['nmalias'],

array('dtiniciomesatual',
'dtfimmesatual',
'dtiniciomespassado',
```

## Proof of Concept (POC)
Just access the URL with your PHP code in "gridValoresPopHidden" parameter.

![image](https://github.com/user-attachments/assets/920ea96c-8a15-4ad7-9446-37d842b7a40c)

### Researches
https://www.linkedin.com/in/xvinicius/

https://www.linkedin.com/in/hairrison-wenning-4631a4124/

- OpenXP Research Team
