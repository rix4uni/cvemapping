# CVE-2017-9606
Due to insufficient of checking integrity, authenticity and low user rights on update folder local user can craft fake ViPNet update files
with arbitrary execution code and place them in ViPNet update folder.
After placing fake update files in ViPNet update folder, ViPNet update system executes them with system or local admin rights

3.x - With local admin rights

4.x - With system rights

Affected Versions:

ViPNet Client/Coordinator for windows - All 4.x and 3.x versions lower than 4.3.2 (42442).

ViPNet Client/Coordinator for windows version 2.x not checked due to outdated version, but could be affected.

Recommendations:

Corrected in ViPNet Client/coordinator 4.3.2 (42442) and higher

For other versions could be applied ViPNet SysLocker to avoid this vulnerability
