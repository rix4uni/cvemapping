FROM centos:7.2.1511

MAINTAINER John Kinsella <jlkinsel@gmail.com>

RUN yum install -y httpd php unzip php-mysql && \
    yum clean all

ADD https://github.com/phpcollab/phpcollab/releases/download/v2.5.1/phpCollab-v2.5.1.zip /
RUN cd /var/www/html && \
    unzip /phpCollab-v2.5.1.zip && \
    rm /phpCollab-v2.5.1.zip && \
    chown -R apache /var/www/html

CMD /usr/sbin/httpd -X
