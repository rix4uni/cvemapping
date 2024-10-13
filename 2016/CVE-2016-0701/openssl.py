#!/usr/bin/python3
# -*- coding: utf-8 -*-
__author__ = "Luan Souza"
__credits__ = ["Antonio Costa aka Cooler_"]
#
#
# CHECK CVE-2016-0701
#
#
from subprocess import check_output
import re

listaVuln = ['1.0.2e','1.0.2d', '1.0.2c','1.0.2b','1.0.2a','1.0.2']
versao = (check_output(['pkg-config','--print-provides','openssl']).decode("utf-8").strip()).split()

if versao[2] in listaVuln:
    print('Your version is:{0}, and is present in the list of affected versions \n Read more:https://openssl.org/news/secadv/20160128.txt'.format(versao[2]))
else:
    print('Your version is:{0}, looks you are safe'.format(versao[2]))
