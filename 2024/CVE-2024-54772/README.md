# CVE-2024-54772 (MikroTik RouterOS Username Enum)
This repo contains the exploit for **CVE-2024-54772** which can enumerate valid usernames in Mikrotik routers running RouterOS **v6.43** through **v7.17.1**.

**"mikrotik_routeros_username_enum.py"** Usage: `python3 mikrotik_routeros_username_enum.py <username> <target>`. The outpus will be either a valid or invalid username.

**"mikrotik_routeros_username_enum_wordlist.py"** Usage: `python3 mikrotik_routeros_userenum_wordlist.py <wordlist_path> <target1,target2,...>`. The output will be all the valid usernames for every router ip entered.

Please, note that every username is sent in a seperate tcp session because RouterOS doesn't respond to the requests sent after 3 tries in the same tcp session.

**Reference:** https://www.cve.org/CVERecord?id=CVE-2024-54772
