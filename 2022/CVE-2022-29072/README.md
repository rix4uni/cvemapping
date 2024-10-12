# 7-Zip.chm-mitigiation
7-Zip Mtigation

CVE-2022-29072 

Explaination : 
https://user-images.githubusercontent.com/33525376/163654035-d40ca72a-7dbc-425f-ade2-3820cfababb2.mp4

Author CVE Founder : 
https://github.com/kagancapar/CVE-2022-29072

A vulnerability has been discovered in 7-zip, the popular archiving program. This is an active zero-day vulnerability and is characterized as allowing privilege escalation and command execution. In other words, someone with limited access to your computer would be able to gain higher-level control, usually admin access, to run commands or apps. GitHub user Kagancapar seems to have unearthed this 7-zip Windows vulnerability, and it has reference CVE-2022-29072.

7-zip is a cross-platform app, but this vulnerability is tied to Windows, as it relies on 7-zip's interactivity with the Windows help application, hh.exe. For example, the GitHub readme file for CVE-2022029072 surmises "Windows allows privilege escalation and command execution when a file with the .7z extension is dragged to the Help>Contents area."

This PowerShell Script made due to the CVE-2022-29072 of RCE and Privilege Esecalation with payload mitigation 
Removal of 7-zip.chm file , this PSH script detects if the 7-zip.chm file exsists in the Program Files directory and removes it.

This script made for mitigation , for wide network with several endpoints post this script inside startup folder and force restart all the hosts.



This script works only if the program exists in the Program Files folder.
