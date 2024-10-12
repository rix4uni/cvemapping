#!/bin/bash

set -e

launchctl stop com.apple.tccd
launchctl start com.apple.tccd
tccutil reset All

