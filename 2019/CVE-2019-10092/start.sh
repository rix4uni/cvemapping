#!/bin/bash -x

apachectl start

ruby -rwebrick -rwebrick/https -d -e 'WEBrick::HTTPServer.new(:DocumentRoot => "./", :Port => 443, :SSLEnable => true, :SSLCertName => [["CN", WEBrick::Utils::getservername]] ).start'
