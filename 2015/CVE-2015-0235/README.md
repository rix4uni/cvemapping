# CVE-2015-0235-test
Ansible playbook to **check vulnerability** for [CVE-2015-0235](http://www.openwall.com/lists/oss-security/2015/01/27/9). This is based on the test program provided by the University of Chigago ([link](https://itservices.uchicago.edu/page/ghost-vulnerability)). Ansible will allow you to specify a large number of host machines to test at once.

**This does not patch or restart anything**, it only reports if your systems are affected.

Assumes `gcc` is installed remotely.

# Note!
Please don't just arbitrarily run this on your hosts, read the code first to see what it does :)

## Usage
Requires ansible. Change the `user: your_remote_user` in `ghost.yml:2` to match your remote system(s).

```
pip install ansible
ansible-playbook -i hosts_to_test ghost.yml
```

## Sample output
```
af:ghost aaronfay$ ansible-playbook ghost.yml -i aaron_host

PLAY [all] ******************************************************************** 

GATHERING FACTS *************************************************************** 
ok: [foobar.com]

TASK: [copy the GHOST script to the machine] ********************************** 
ok: [foobar.com]

TASK: [compile it] ************************************************************ 
ok: [foobar.com]

TASK: [run it!] *************************************************************** 
ok: [foobar.com]

TASK: [show me the results] *************************************************** 
ok: [foobar.com] => {
    "ghost.stdout_lines[0]": "vulnerable"
}

PLAY RECAP ******************************************************************** 
foobar.com                 : ok=5    changed=0    unreachable=0    failed=0   
```
