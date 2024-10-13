FROM ubuntu:16.04

WORKDIR /minidlna

################
# PREREQUISITES
################

RUN apt-get update 

RUN apt-get install -y \
build-essential \
gettext \
sudo \
nano \
gdb

RUN apt-get install -y \
libexif-dev \
libjpeg-dev \
libid3tag0-dev \
libflac-dev \
libvorbis-dev \ 
libsqlite3-dev \
libavformat-dev \
uuid-dev \
uuid-runtime \
libuuid1 && \
apt-get clean && rm -rf /var/lib/apt/lists/*

########
# BUILD
########

COPY minidlna-1.2.1 .

RUN ./configure && make && make install
RUN cp ./minidlna.conf /etc/minidlna.conf
