## This is the first version of the "weaponized" exploit for `CVE-2016-6210`

### Background:
Posted by Eddie Harari on Full Disclosure 
http://seclists.org/fulldisclosure/2016/Jul/51

###### The brief:
>By sending large passwords, a remote user can enumerate users on system that runs SSHD. This problem exists in most 
modern configuration due to the fact that it takes much longer to calculate SHA256/SHA512 hash than BLOWFISH hash.

###### The (more) technical:
>When SSHD tries to authenticate a non-existing user, it will pick up a fake password structure hardcoded in the SSHD 
source code. On this hard coded  password  structure  the password hash is based on BLOWFISH ($2) algorithm.
If real users passwords are hashed using SHA256/SHA512, then sending large passwords (10KB) will result in shorter 
response time from the server for non-existing users.

**NOTE: Mr. Harari tested this on `opensshd-7.2p2`, while my testing was done on  `OpenSSH_6.9p1`.** 

The script is currently based around a 10-30% range of deviation for timing(s) of valid versus invalid usernames. Currently only >20% are accepted as a valid usernames and appended to the output list accordingly (feel free to tweak this within the script). This has proved effective for me.

* More information on the process/background: https://justifysecurity.com/blog/weaponizing-cve-2016-6210/

`Bringing this project over to Github from Bitbucket.`
