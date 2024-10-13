FROM debian:jessie

MAINTAINER t0kx <t0kx@protonmail.ch>

# install debian stuff
RUN apt-get update && \
    apt-get upgrade -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    wget curl openjdk-7-jre-headless && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# configure vuln application
RUN wget https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.4.2.tar.gz && \
    tar xfz elasticsearch-1.4.2.tar.gz && \
    mv elasticsearch-1.4.2 elasticsearch

EXPOSE 9200

COPY main.sh /
ENTRYPOINT ["/main.sh"]
CMD ["default"]
