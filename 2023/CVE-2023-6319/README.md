# Root my webOS TV

A simple python script that starts a telnet server on vulnerable webOS devices as `root`.

## Supported TVs

- **webOS 4.9.7 - 5.30.40** (model **LG43UM7000PLA**)
- **webOS 5.5.0 - 04.50.51** (model **OLED55CXPUA**)
- **webOS 6.3.3-442 (kisscurl-kinglake) - 03.36.50** (model **OLED48C1PUB**)
- **webOS 7.3.1-43 (mullet-mebin) - 03.33.85** (model **OLED55A23LA**)

## Installation

1. Install Python 3 from https://www.python.org/downloads/ or using a package manager
2. Clone this repo
3. Install dependencies using `pip install -r requirements.txt`
4. Run the script using `python rootmytv.py`
5. Follow on-screen instructions

If the script was successful, a telnet server with root access will be created on the TV with port 23. You can use any software to access it, for example Putty on Windows.

A more in-depth tutorial can be found on my blog here: https://blog.illixion.com/2024/04/root-lg-webos-tv/

## Known errors

- `500 application error, not allowed to call com.webos.service.downloadmanager/download`: your TV is patched against this vulnerability and is thus incompatible
- `websockets.exceptions.InvalidMessage: did not receive a valid HTTP response`: you are using an old version of the script, please redownload all files, reinstall the requirements and try again


## References

This exploit uses the following CVE: https://www.cve.org/CVERecord?id=CVE-2023-6319