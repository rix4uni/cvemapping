# CVE-2014-8731-PoC - PHPMemcachedAdmin Remote Code Execution
A proof of concept tool to test your own system if they are vulnerable to CVE-2014-8731

## Blog Post

[PHPMemcachedAdmin Remote Code Execution - CVE-2014-8731 PoC](https://netw0rk.io/blog/phpmemcachedadmin-remote-code-execution-cve-2014-8731-poc/)

## Run test

Start victim server:
```bash
docker run -p8081:80 --rm --name phpma -it alphayax/phpmemcachedadmin
```

Attack victim with PoC:
```bash
git clone https://github.com/sbani/CVE-2014-8731-PoC.git
cd CVE-2014-8731-PoC
python attack.py http://localhost:8081 id
```

## CVE details
> PHPMemcachedAdmin 1.2.2 and earlier allows remote attackers to execute arbitrary PHP code via vectors related "serialized data and the last part of the concatenated filename," which creates a file in webroot.

References:
- https://nvd.nist.gov/vuln/detail/CVE-2014-8731
