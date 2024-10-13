FROM debian:jessie

MAINTAINER t0kx <t0kx@protonmail.ch>

# install debian stuff
RUN apt-get update && \
    apt-get upgrade -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    wget vim build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# configure vuln application
RUN wget https://www.sudo.ws/dist/sudo-1.8.13.tar.gz -O /tmp/sudo.tar.gz && \
    tar xfz /tmp/sudo.tar.gz -C /tmp/ && \
    cd /tmp/sudo-1.8.13 && \
    ./configure && \
    make && make install
RUN rm -rf /tmp/sudo*

# create default user
RUN useradd -d /home/user \
    -s /bin/bash \
    -ms /bin/bash user

# add sudoers entry
RUN echo 'user ALL=NOPASSWD: sudoedit /home/*/*/esc.txt' >> /etc/sudoers

COPY exploit.sh /home/user/
RUN chmod +x /home/user/exploit.sh

# run interactive shell
# with user privileges
CMD ["su", "-", "user"]
