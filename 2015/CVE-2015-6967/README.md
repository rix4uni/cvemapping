# CVE-2015-6967

Nibbleblog 4.0.3 - Arbitrary File Upload (CVE-2015-6967)

## requirements

- python 3
- `requests`

## usage

```
usage: exploit.py [-h] --url URL --username USERNAME --password PASSWORD --payload PAYLOAD

optional arguments:
  -h, --help            show this help message and exit
  --url URL, -l URL
  --username USERNAME, -u USERNAME
  --password PASSWORD, -p PASSWORD
  --payload PAYLOAD, -x PAYLOAD
```

example:

`python3 exploit.py --url http://10.10.10.75/nibbleblog/ --username admin --password nibbles --payload shell.php`

