# PoC-CVE-2024-44349

Vulnerability found and tested in **Anteeo WMS - v4.7.31**

The vulnerability allows threat actors to craft an SQL command inside the username parameter and disclose data in the underlying database. 
The impacted versions of ANTEEO B2B WMS are from v.4.7.x to v.4.7.34 (excluded).


## Usage
1. `git clone git@github.com:AndreaF17/PoC-CVE-2024-44349.git`
2. `cd PoC-CVE-2024-44349`
3. `python3 -m venv venv`
4. `source venv/bin/activate`
5. `pip3 install -r requirements.txt`
6. `python3 ./main.py -t TARGET -m [MODE]`
### Modes
Before starting a MODE the script check if ANTEEO is vulnerable and procedes.
The available modes are:
- **dump**: `python3 ./main.py -t TARGET -m dump`, dumps the DB.
- **query**: `python3 ./main.py -t TARGET -m query`, opens a shell where you can send SQL query on the server.

## Utils Directory
Inside the `utils/utils.py` there are some functions to extract data from the DB.

# Terms of Use
This PoC was developed for research and educational purposes only. It is provided "as-is," without any warranties, and the author takes no responsibility for any damage caused by its use.

By using this PoC, you agree that:
- It should only be used in environments you own or have explicit permission to test.
- Any misuse, illegal, or unethical use is strictly prohibited.
- The author will not be liable for any direct, indirect, or incidental damages arising from its use.

Use at your own risk and ensure compliance with applicable laws.
