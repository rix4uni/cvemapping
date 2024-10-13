# CVE-2021-21809 POC

CVE details: A command execution vulnerability exists in the default legacy spellchecker plugin in Moodle 3.10. A specially crafted series of HTTP requests can lead to command execution. An attacker must have administrator privileges to exploit this vulnerabilities.

In the below video, I'm going to gain access to Golden Eye 1 OSCP Lab by exploiting this vulnerability with out using Metasploit. Check out GoldenEye 1: https://www.vulnhub.com/entry/goldeneye-1,240/.

Get the revershell by using telnet command, encode it as url format and save it to `Path to aspell` (Settings/Server/System paths).

https://user-images.githubusercontent.com/101538840/208561898-6468a4ef-acf8-4742-b3e1-f0955ae7e9ab.mp4
