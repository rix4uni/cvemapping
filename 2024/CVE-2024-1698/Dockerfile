FROM wordpress:apache

RUN apt-get update \
    && apt-get install -y vim wget unzip

RUN cd /tmp \
    && wget https://downloads.wordpress.org/plugin/notificationx.2.8.2.zip \
    && unzip notificationx.2.8.2.zip \
    && mv /tmp/notificationx /usr/src/wordpress/wp-content/plugins/ \
    && rm /tmp/notificationx.2.8.2.zip