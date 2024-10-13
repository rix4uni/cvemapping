FROM debian:buster

ENV CACTI_VERSION 1.2.8

RUN apt-get -y -q update; \
    apt-get -y -q install apache2 xxd nano git unzip wget php php-simplexml php-gd php-ldap php-zip php-imap php-mysql php-mbstring php-gmp php-snmp mariadb-client mariadb-server rrdtool; \
    ln -s /usr/bin/rrdtool /usr/local/bin/rrdtool

# Download and install cacti
RUN wget -q https://files.cacti.net/cacti/linux/cacti-${CACTI_VERSION}.tar.gz -O /tmp/cacti.tar.gz \
    && cd /var/www/html/ \
    && rm /var/www/html/index.html \
    && tar xf /tmp/cacti.tar.gz \
    && mkdir -p ./cacti/ \
    && mv ./cacti-${CACTI_VERSION}/* ./cacti/; rm -rf ./cacti-${CACTI_VERSION}/ \
    && rm -rf /tmp/cacti.tar.gz

RUN chown www-data: -R /var/www/

# Configure PHP
RUN for php_version in $(ls /etc/php/); do \
      for ini_file in $(find /etc/php/${php_version}/ -name "php.ini"); do \
        sed -i 's/[;]\?[ ]*memory_limit[ ]*=[ ]*.*/memory_limit = 400M/g' ${ini_file}; \
        sed -i 's/[;]\?[ ]*max_execution_time[ ]*=[ ]*.*/max_execution_time = 60/g' ${ini_file}; \
        sed -i 's/[;]\?[ ]*date.timezone[ ]*=[ ]*.*/date.timezone = Europe\/Paris/g' ${ini_file}; \
      done \
    done

# Configure mysql
RUN service mysql start \
    && mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root mysql \
    && mysqladmin -uroot create cacti \
    && mysql -uroot -e "grant all on cacti.* to 'cactiuser'@'localhost' identified by 'cactiuser'" \
    && mysql -uroot -e "grant select on mysql.time_zone_name to 'cactiuser'@'localhost' identified by 'cactiuser'" \
    && mysql -uroot cacti < /var/www/html/cacti/cacti.sql

RUN echo "#!/bin/bash" > /entrypoint.sh ;\
    echo "service mysql start" >> /entrypoint.sh ;\
    echo "apachectl -D FOREGROUND" >> /entrypoint.sh ;\
    chmod +x /entrypoint.sh

EXPOSE 80

CMD /entrypoint.sh
