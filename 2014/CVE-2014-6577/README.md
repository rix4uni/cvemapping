# oracle-xxe-sqli
Automated Oracle CVE-2014-6577 exploitation via SQLi

## Usage:
```
oracle-xxe-sqli.py [-h] [-i IP] [-p PORT] [--disable-server] [--custom-headers CUSTOM_HEADERS] 
                   [-f PAYLOAD_FILE] url

Options

positional arguments:

  url                   	URL to inject. Use * as the injection marker, just once.

optional arguments:

  -h, --help                              Show this help message and exit
  -i IP, --ip IP        		  Public ip. Useful for port forwarding. Default is this machine’s ip. (default: x.x.x.x)
  -p PORT, --port PORT  		  Port to use. Default will be chosen at random between 10000 and 20000. (default: *generated*)
  --disable-server      		  Don't start server (default: False)
  --custom-headers CUSTOM_HEADERS	  Pass a json dictionary with the custom headers. (default: None)
  -f PAYLOAD_FILE, --payload-file	  PAYLOAD_FILE
                        		  File to extract the SQL queries from (default: payloads.lst)
```
