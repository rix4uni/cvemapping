#!/bin/bash

sudo apt-get install git libcups2-dev cups -y
git clone https://github.com/referefref/cupspot-2024-47177.git
cd cupspot-2024-47177
pip3 install -r requirements.txt --break-system-packages
systemctl enable cups
systemctl start cups
