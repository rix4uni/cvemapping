FROM openjdk:11.0.9.1-jre-buster

RUN apt update && apt install -y lsof

ARG SOLR_VER=8.2.0
ENV PATH $PATH:/usr/local/src/solr-${SOLR_VER}/bin

WORKDIR /usr/local/src
RUN curl -OL https://archive.apache.org/dist/lucene/solr/${SOLR_VER}/solr-${SOLR_VER}.tgz
RUN tar -xzvf solr-${SOLR_VER}.tgz

RUN apt update && apt install -y procps

WORKDIR /usr/local/src/solr-${SOLR_VER}/bin
