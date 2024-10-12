#!/bin/sh
cp ./screenshot ./screenshot_copy
./screenshot_copy & sleep 1 && rm screenshot_copy
