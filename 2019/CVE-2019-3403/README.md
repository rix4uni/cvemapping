# CVE-2019-3403
I wanted to easily be able to exploit CVE-2019-3403 to scrape all the users from a JIRA application, so I threw this script together. It isn't the cleanest code ever, and it doesn't handle requests that return over 1000 users (it will just truncate them to the first 1000) - but it can quickly scrape all of the users from a vulnerable JIRA server.

## Usage
```
usage: scrape_jira.py [-h] -d DOMAIN [-q QUERY] [-o OUT] [-v]

Scrape User Information from Vulnerable JIRA Instances [CVE-2019-3403]

optional arguments:
  -h, --help            show this help message and exit
  -d DOMAIN, --domain DOMAIN
                        The domain of the target
  -q QUERY, --query QUERY
                        Specific query to run against the API
  -o OUT, --out OUT     Output to a file
  -v, --verbose         Verbose output
```

### Examples
Scrape everything and save output to a file:
```
python3 CVE-2019-3403.py -d jira.example.com -o out.txt -v
```

Just look for a specific user:
```
python3 CVE-2019-3403.py -d jira.example.com -q admin
```