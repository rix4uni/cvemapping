FROM httpd:2.2

COPY ./my-httpd.conf /usr/local/apache2/conf/httpd.conf
COPY ./start.sh /usr/local/start.sh

RUN apt-get update && apt-get install -y ruby

RUN chmod +x /usr/local/start.sh

CMD ["/usr/local/start.sh"]
