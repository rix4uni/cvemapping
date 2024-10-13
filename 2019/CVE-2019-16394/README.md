# CVE-2019-16394

A simple POC python script of CVE-2019-16394

Script is adjusted for a french website, you may need to modify it if the website language is different.

## Install

```bash
pip install -r requirements.txt
```

## Usage

```bash
usage: cve_2019_16394.py [-h] -u URL -f FILE [-v]

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     Base Target URL (without the spip.php)
  -f FILE, --file FILE  File containing the mails to test
  -v, --verbose         Verbose output
```

## Links

https://www.cvedetails.com/cve/CVE-2019-16394/
https://zone.spip.net/trac/spip-zone/changeset/117577/spip-zone
