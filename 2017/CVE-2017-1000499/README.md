# 5MMISSI-CVE-2017-1000499

### PoC of [CVE-2017-1000499](https://www.cvedetails.com/cve/CVE-2017-1000499/?q=CVE-2017-1000499)
phpMyAdmin versions 4.7.x (prior to 4.7.6.1/4.7.7) are vulnerable to a CSRF weakness. By deceiving a user to click on a crafted URL, it is possible to perform harmful database operations such as deleting records, dropping/truncating tables etc. 

### Contents
- Makefile
- web/index.html

### Instructions
#### Getting all prepared

```shell
git clone https://github.com/Villaquiranm/5MMISSI-CVE-2017-1000499.git
cd 5MMISSI-CVE-2017-1000499/
```
#### Building docker enviroment
To build both containers you only need to type a single command.
```shell
make create
```
At this point it is necessary to wait because php server and database need to be configurated. This delay is approximately one minute after a successful build.

#### Experimenting with your exploid
1. First go to [Localhost](http://localhost/).
2. Type root as user and password. (if you get an error it is because server is still configurating itself).
3. Observe carefully all your database schemas.

4. Assuming you are still in this repository. We will create a Python server to exploit this vulnerability.
```shell
cd web/
python -m SimpleHTTPServer 8888
```
5. Go to [Localhost:8888](http://localhost:8888/).
6. Reaload your database page (localhost).
#### Destroying docker enviroment
```shell
make clean
```
