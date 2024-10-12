# CVE-2024-1931-reproduction

CVE-2024-1931复现docker环境以及漏洞触发脚本



使用方式

docker构建镜像

```
docker build -t unbound1.19.1-image .
```

创造容器

```
docker run -d -t -i -p 53:53/udp -p 53:53/tcp --name=unbound1.19.1-container <image-hash> /bin/bash
```

进入容器

```
docker exec -it <container-hash> /bin/bash
```



进入容器后

执行命令启动unbound服务

```
unbound
```

容器内运行exploit.sh触发DOS漏洞

```
./exploit.sh
```

