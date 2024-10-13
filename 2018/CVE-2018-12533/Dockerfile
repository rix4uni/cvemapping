FROM andreptb/maven:3.2.5

RUN apt update
RUN apt install unzip -y
RUN wget http://downloads.jboss.org/richfaces/releases/3.3.X/3.3.4.Final/richfaces-examples-3.3.4.Final.zip
RUN wget https://sourceforge.net/projects/jboss/files/JBoss/JBoss-5.1.0.GA/jboss-5.1.0.GA-jdk6.zip
RUN unzip richfaces-examples-3.3.4.Final.zip
RUN unzip jboss-5.1.0.GA-jdk6.zip
RUN mv richfaces-examples-3.3.4.Final/photoalbum/dist/photoalbum-ear-3.3.4.Final.ear jboss-5.1.0.GA/server/default/deploy/

EXPOSE 8080
EXPOSE 8009

CMD ["/data/jboss-5.1.0.GA/bin/run.sh", "-b", "0.0.0.0"]