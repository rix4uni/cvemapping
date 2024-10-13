#!/bin/sh

docker build -t minidlna .
docker run --name minidlna --security-opt seccomp=unconfined -p 8200:8200 -it minidlna

