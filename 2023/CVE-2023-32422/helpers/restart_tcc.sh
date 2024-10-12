#!/bin/bash

echo "[+] Restarting TCC"
launchctl stop com.apple.tccd
launchctl start com.apple.tccd

