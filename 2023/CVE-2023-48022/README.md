# PoC for a remote command execution vulnerability in Ray framework (CVE-2023-48022)

This exploit script and PoC are written for an in-depth CVE analysis on [vsociety](https://www.vicarius.io/vsociety/posts/the-story-of-shadowray-cve-2023-48022).

The Ray framework, an essential tool for Python-based AI and machine learning applications, has encountered a significant security challenge. In essence, Ray is like a Swiss Army knife for people working on AI and big data projects. Identified as CVE-2023-48022, this vulnerability specifically impacts the job submission API. The official description states that this flaw allows a remote attacker to execute arbitrary code, posing a considerable risk to systems utilizing these versions of Ray. This vulnerability's discovery has underscored the importance of robust security protocols in software frameworks, especially those integral to AI and ML projects with vast data and computational power.

## Usage

First, install Ray:
```bash
pip3 install -U "ray[default]"==2.8.0
```
Then, start Ray:
```bash
ray start --head --dashboard-host=0.0.0.0
```
Run the Python exploit:
```bash
python3 exploit.py --host http://192.168.150.16:8265 --cmd '<cmd>'
```
## Metasploit module
Copy the Ruby file to Metasploit's related folder:
```bash
cp ray_job_rce.rb /usr/share/metasploit-framework/modules/exploits/multi/misc/
```
Launch Metasploit with `msfconsole` and relad modules with `reload_all` if you can't find the added one.
You can select with `use exploit/multi/misc/ray_job_rce`.
Set the necessary options (`RHOST`, `RPORT`, `COMMAND`, etc.) and run the exploit with the command `exploit`.

## Disclaimer
This exploit script has been created solely for research and the development of effective defensive techniques. It is not intended to be used for any malicious or unauthorized activities. The script's author and owner disclaim any responsibility or liability for any misuse or damage caused by this software. Just so you know, users are urged to use this software responsibly and only by applicable laws and regulations. Use responsibly.
