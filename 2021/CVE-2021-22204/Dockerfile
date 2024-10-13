FROM ubuntu

LABEL maintainer="unicord@unicord.dev"

WORKDIR /opt/exploit-CVE-2021-22204

RUN apt update
RUN apt install -y djvulibre-bin perl zip wget make python3 file
RUN wget https://github.com/exiftool/exiftool/archive/refs/tags/12.23.zip
RUN unzip 12.23.zip
WORKDIR /opt/exploit-CVE-2021-22204/exiftool-12.23
RUN perl Makefile.PL
RUN make test
RUN make install
RUN rm 12.23.zip
RUN rm -rf exiftool-12.23
WORKDIR /opt/exploit-CVE-2021-22204

COPY . .

ENTRYPOINT ["/bin/bash"]