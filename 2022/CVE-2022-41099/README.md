# Update Windows RE - CVE-2022-41099
Script to update Windows Recovery Environment to patch against CVE-2022-41099. The script pulls the January CU for each build, mounts WinRE, updates it, saves WinRE, then verifies the build number matches what the January CU is. *Win10-21H1's last CU was Dec 2022 so that version pulls the Dec 22 CU*<br />
Supported OS and Builds: Windows 11 (22H2 & 21H2) & Windows 10 (22H2, 21H2, 21H1, & 20H2). Unsure if LTSC will work. <br />
Built with help from comments of reddit users /u/shiz0_ and /u/DrunkMAdmin and u/JoseEspitia_com <br />
No warranty implied. Do your own testing prior to running. <br />
