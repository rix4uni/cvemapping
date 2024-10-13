# PHP CGI Argument Injection (CVE-2012-1823)

[![PHP](https://img.shields.io/badge/PHP%20-%20%3C%205.3.12%20%2F%20%3C%205.4.2%20-%20%23777BB3?logo=php&logoColor=white&link=https%3A%2F%2Fwww.php.net%2Fmanual)](https://www.php.net/manual)
[![CVE](https://img.shields.io/badge/CVE--2012--1823%20-%20%23FCB417)](https://www.cve.org/CVERecord?id=CVE-2012-1823)

## Description
> sapi/cgi/cgi_main.c in PHP before 5.3.12 and 5.4.x before 5.4.2, when configured as a CGI script (aka php-cgi), does not properly handle query strings that lack an = (equals sign) character, which allows remote attackers to execute arbitrary > code by placing command-line options in the query string, related to lack of skipping a certain php_getopt for the 'd' case.

## Usage
```
./php_cgi.sh http://<RHOST> <COMMAND>
```

## Example
```
./php_cgi.sh http://10.128.20.2 "whoami"
```
![Proof of concept](images/poc.png)
