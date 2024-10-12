# CVE-2023-50254 - Deepin Linux's default document viewer deepin-reader RCE
CVE-2023-50254: PoC Exploit for Deepin-reader RCE that affects unpatched Deepin Linux Desktops. Deepin Linux's default document reader "deepin-reader" software suffers from a serious vulnerability due to a design flaw that leads to Remote Command Execution via crafted docx document.

Details

Deepin-reader is the default document reader for the Operating System Deepin Linux. The deepin-reader performs some shell command operations while dealing with docx document format.

1. When opening a docx document , deepin-reader creates a temporary directory under /tmp and places the docx document under the directory

2. Then deepin-reader calls the "unzip" shell command to extract the docx file

3. After the extraction process, deepin-reader calls "pandoc" command to convert the docx file to an html file named "temp.html" under word/ directory (created when the docx file is extracted with unzip). The command will look something like this, "pandoc temp.docx -o word/temp.html

4. Then deepin-reader will try to convert that HTML file to pdf and open the pdf.

This happens when we open a docx file in Deepin Linux OS.
![image](https://github.com/febinrev/deepin-linux_reader_RCE-exploit/assets/52229330/57fed21a-025b-44d6-83fc-1ab51b2a8946)

This behavior can be exploited by placing a symlink named word/temp.html inside a crafted malicious docx pointing to any file inside the target system.

So, while opening the docx file, pandoc will write to the system file that the symlink word/temp.html is pointing to.


This is a File overwrite vulnerability.
A Remote Code Execution can be achieved by overwriting files like .bash_rc, .bash_login, etc. Rce will be triggered when the user opens the terminal.


Advisory: https://github.com/linuxdeepin/developer-center/security/advisories/GHSA-q9jr-726g-9495
