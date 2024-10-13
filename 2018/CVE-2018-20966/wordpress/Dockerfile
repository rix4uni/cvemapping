# use the official wordpress Docker image
FROM wordpress:5.1.1

# install curl and jq
RUN apt-get update
RUN apt clean && apt update && apt install -y jq curl unzip wget vim nano
RUN echo "upload_max_filesize = 40M" > /usr/local/etc/php/php.ini && echo "post_max_size = 40M" >>   /usr/local/etc/php/php.ini

# install wp cli
RUN curl -o /bin/wp https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar && chmod +x /bin/wp

# install woocommerce
RUN wget https://downloads.wordpress.org/plugin/woocommerce.4.7.1.zip && unzip *.zip -d /usr/src/wordpress/wp-content/plugins/

# install quickview
RUN wget https://downloads.wordpress.org/plugin/woocommerce-jetpack.3.7.0.zip && unzip "woocommerce-jetpack.3.7.0.zip" -d /usr/src/wordpress/wp-content/plugins/

###
# setup wordpress
###

# this auto creates the site and enables all plugins
RUN sed -i 's/exec "$@"/wp --allow-root core install --path="\/var\/www\/html" --url=localhost --title="WordPress site" --admin_user="admin" --admin_password="admin" --admin_email="admin@abc.com"/g' /usr/local/bin/docker-entrypoint.sh
RUN echo 'wp --allow-root plugin activate --all' >> /usr/local/bin/docker-entrypoint.sh
RUN echo 'chmod -R 777 /var/www/html/wp-content/' >> /usr/local/bin/docker-entrypoint.sh
RUN echo 'exec "$@"' >> /usr/local/bin/docker-entrypoint.sh