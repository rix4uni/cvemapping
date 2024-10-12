#!/bin/bash

launchctl stop com.apple.tccd
launchctl start com.apple.tccd
sleep 1
tccutil reset All
ls -al ~/Library/Application\ Support/com.apple.TCC/TCC.db

