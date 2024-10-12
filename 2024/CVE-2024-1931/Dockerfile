# 使用 Ubuntu 22.04 作为基础镜像
FROM ubuntu:22.04

# 备份原始的 sources.list 文件
RUN cp /etc/apt/sources.list /etc/apt/sources.list.bak
# 替换为指定的镜像源（这里以清华大学镜像源为例）
RUN sed -i 's/archive.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list

# 更新系统包并安装必要的工具和依赖项
RUN apt-get update && \
    apt-get install -y wget unzip dnsutils build-essential libssl-dev \
                       libexpat1-dev flex bison libevent-dev && \
    # 下载并解压 Unbound 源代码
    wget https://github.com/NLnetLabs/unbound/archive/refs/tags/release-1.19.1.zip && \
    mkdir unbound && \ 
    unzip release-1.19.1.zip -d /unbound && \
    cd /unbound/unbound-release-1.19.1 && \
    # 编译并安装 Unbound
    ./configure && \
    make && \
    make install && \
    ldconfig   && \
    # # 清理无用文件以减小镜像体积
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# 添加 unbound 用户
RUN adduser --system --no-create-home --group unbound

# 复制 data 文件夹的内容到 /usr/local/etc/unbound/
COPY data/ /usr/local/etc/unbound/

# 配置 Unbound
WORKDIR /usr/local/etc/unbound/

RUN  cp unbound.conf unbound.conf.example &&\
     cp unbound.conf.exploit unbound.conf

RUN pwd 

RUN  mkdir -p var && \
     chmod 777 var && \
     touch unbound.log && \
     chmod 777 unbound.log && \
     touch var/root.key && \
     chmod 777 var/root.key

# unbound-anchor 返回非0退出代码     
RUN     unbound-anchor -a ./var/root.key || true


# 暴露默认 DNS 端口
EXPOSE 53/tcp 53/udp

# 设置容器启动时的默认命令为 shell
CMD ["/bin/bash"]
