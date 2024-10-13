
**CVE-2021-31233**
- Software Name
	- Fighting Cock Information System v1.0

- Vulnerability Type
	 - SQL Injection

- Attack Type
	- Remote

- Impact
	- Information Disclosure

- Description
	- A remote, unauthenticated attacker can retrieve database information by exploiting a SQL injection vulnerability in the edit_breed.php page via the id variable

- Software Link
	- [https://www.sourcecodester.com/php/12824/fighting-cock-information-system.html](https://www.sourcecodester.com/php/12824/fighting-cock-information-system.html)

- Vendor
	- Source Codester

- Vulnerable Codebase
	- v1.0

- Vulnerable Code Block
	- file: /FCIS/admin/pages/tables/edit_breed.php
```
<!DOCTYPE html>
<html>

<?php include('header.php');?>



<?php

error_reporting(1);
$id = $_GET['id'];
include '../../../config/db_config.php';

$sql = "SELECT * FROM breeders where breeder_id = '$id' ";
$result = $conn->query($sql);

...

```
