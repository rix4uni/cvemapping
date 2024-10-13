FROM ubuntu
MAINTAINER ptantiku

RUN apt-get update
RUN apt-get upgrade -y 
RUN apt-get install -y wget unzip
RUN apt-get install -y apache2 libapache2-mod-php5 mongodb php5-mongo
RUN apt-get install -y openssh-server

# download phpmoadmin
WORKDIR /var/www/html
RUN wget http://www.phpmoadmin.com/file/phpmoadmin.zip
RUN unzip phpmoadmin.zip

#enable login, scott/tiger
RUN sed -i -re 's%^//(\$accessControl.*)$%\1%g' moadmin.php

EXPOSE 22 80
#[optional] add vhost
#ADD my_vhost.conf /etc/apache2/sites-enabled/

#set default run command
ADD run.sh /run.sh
CMD ["/run.sh"]
