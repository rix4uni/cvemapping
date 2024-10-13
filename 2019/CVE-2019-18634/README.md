# CVE-2019-18634

**:warning: This code has only been tested on sudo 1.8.25. The bug impacts <1.8.30, but there are differences in character handling that prevent this PoC from executing (this does not mitigate the exploitability of the bug). See [#1](https://github.com/Plazmaz/CVE-2019-18634/issues/1) :warning:**  
  
Functional exploit for CVE-2019-18634, a heap buffer overflow that leads to privilege escalation on sudo <=1.8.30 if pwfeedback is enabled.  
[https://dylankatz.com/Analysis-of-CVE-2019-18634/](https://dylankatz.com/Analysis-of-CVE-2019-18634/)  
This repo contains both a single-file script (`self-contained.sh`), and the scripts used to generate it (under `src`)  
Thanks to yuu and Anonymous_ for help in developing this exploit and these scripts.  
Credit to Joe Vennix and William Bowling for the original discovery of the bug and the information on exploiting through 1.8.30.  
