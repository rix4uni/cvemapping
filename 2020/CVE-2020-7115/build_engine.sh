#!/bin/bash

gcc_installed=$(command -v gcc)

if [[ $(id -un) == "root" ]];
    then
        if [[ ${#gcc_installed} -eq 0 ]];
            then
                $(apt-get update && apt-get install gcc -y && apt-get install apt-utils && apt-get install libssl-dev)
            else
                $(mkdir output)
                $(gcc -fPIC -o output/engine.o -c engine.c && gcc -shared -o output/engine.so -lcrypto output/engine.o)
                $(rm output/*.o)
        fi
    else
        echo -e "\nDeber ser root para ejecutar este script.\n"
fi
# By Retr0
