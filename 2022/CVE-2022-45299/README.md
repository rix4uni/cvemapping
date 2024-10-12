# CVE-2022-45299
#Affected Library :

webbrowser.rs before version 0.8.3
https://github.com/amodm/webbrowser-rs

#Summary:

The library fails to validate that the provided input is actually an URL. An attacker in control of an unfiltered URL passed to webbrowser::open(URL) can, therefore, provide a local file path that will be opened in the default explorer or pass one argument to the underlying open command to execute arbitrary registered system commands.

#Details:

webbrowser::open internally calls shellExecuteW passing in the URL as an arg to open for Windows.On windows, the attacker controls the lpFile argument to shellExecuteW which may allow opening arbitrary local files.
If an attacker manages to pass in an URL that is actually a command line switch to open, they may be able to launch arbitrary commands (or do whatever open allows them to do with one argument). For example, webbrowser::open(".") will open Finder in the current working dir. Also you can execute python scripts by just providing the path to the scriptand I managed to do that with any other language compiled or scripting. I couldn't reproduce the issue on linux but local files like /etc/passwd can be loaded by just providing the path to the file.

#vuln code:
![vuln_code](https://user-images.githubusercontent.com/110370549/212315121-08c4d980-d9cc-45ef-8072-9de18cfb312a.png)

#POC:
![rev_shell](https://user-images.githubusercontent.com/110370549/212315100-351e70c4-f58d-472f-aab8-a883469dbafd.png)

