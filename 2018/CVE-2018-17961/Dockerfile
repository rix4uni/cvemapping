FROM debian:sid
ENV SSH_PASSWORD "rootpass"

RUN apt-get -qq update
RUN apt-get install -qq -y supervisor openssh-server

# Install SSH access
RUN mkdir /var/run/sshd
RUN echo "root:$SSH_PASSWORD" | chpasswd
RUN sed -i 's/^.*PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN echo "X11UseLocalhost no" >> /etc/ssh/sshd_config
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd
# Configure supervisor
RUN mkdir -p /var/log/supervisor
RUN echo "[supervisord]" >> /etc/supervisor/conf.d/supervisord.conf
RUN echo "nodaemon=true" >> /etc/supervisor/conf.d/supervisord.conf
RUN echo "[program:sshd]" >> /etc/supervisor/conf.d/supervisord.conf
RUN echo "command=/usr/sbin/sshd -D" >> /etc/supervisor/conf.d/supervisord.conf

RUN echo 'deb http://snapshot.debian.org/archive/debian/20181002T153836Z/ sid main contrib non-free' > /etc/apt/sources.list

RUN apt-get -qq -o 'Acquire::Check-Valid-Until=false' update
RUN apt-get -qq -y install evince firefox ghostscript

WORKDIR /root/

COPY executeonly_bypass_ps.bin executeonly_bypass.ps

EXPOSE 22

CMD [ "/usr/bin/supervisord", "-c",  "/etc/supervisor/conf.d/supervisord.conf" ]
