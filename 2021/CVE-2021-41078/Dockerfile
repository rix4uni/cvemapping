FROM python:3.6-bullseye

WORKDIR /nameko
COPY ./ /nameko/
RUN pip install nameko==2.13.0
CMD ["nameko","run","--config","malicious.yml","test"]