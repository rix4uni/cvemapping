
FROM debian
WORKDIR /slipper
RUN apt update
RUN apt install -y git python3 python3-pip
RUN pip3 install py7zr==0.20.0
RUN git clone https://github.com/0xless/CVE-2022-44900-demo-lab.git .
EXPOSE 9999
CMD ["python3", "slipper.py"]
