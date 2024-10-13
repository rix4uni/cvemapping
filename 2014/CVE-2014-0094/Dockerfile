FROM vulhub/java:7u55-jdk
#FROM openjdk:7-jre

WORKDIR /tmp

RUN echo "deb http://archive.debian.org/debian/ stretch main" > /etc/apt/sources.list \
    && echo "deb http://archive.debian.org/debian-security stretch/updates main" >> /etc/apt/sources.list \
    && apt-get update \
    && apt-get install -y zip

# 名前解決結果で当たりはずれあるみたいなので、--timeout で3秒ごとにサーバを変更
RUN wget https://archive.apache.org/dist/tomcat/tomcat-8/v8.0.5/bin/apache-tomcat-8.0.5.tar.gz  --timeout 3 -t 1 && \
    tar xvzf apache-tomcat-8.0.5.tar.gz && \
    mv apache-tomcat-8.0.5 /usr/local/tomcat && \
    chmod +x /usr/local/tomcat/bin/catalina.sh
RUN wget https://archive.apache.org/dist/struts/binaries/struts-2.3.16-all.zip --timeout 3 -t 1 && \
    unzip struts-2.3.16-all.zip && \
    cp ./struts-2.3.16/apps/struts2-blank.war /usr/local/tomcat/webapps
RUN rm -rf /tmp/*

EXPOSE 8080

CMD ["/usr/local/tomcat/bin/catalina.sh", "run"]
