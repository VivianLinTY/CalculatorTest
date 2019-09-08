#!/bin/bash

if [ ! -d /sdcard/testFiles/errorLog ]; then
  mkdir -p /sdcard/testFiles/errorLog;
fi

now="$(date +'%Y%m%d%s')"
mkdir -p /sdcard/testFiles/errorLog/$now
screencap -p /sdcard/testFiles/errorLog/$now/screenshot.jpg  
logcat -v time > /sdcard/testFiles/errorLog/$now/logcat &

sleep 10
killall logcat

dumpsys meminfo > /sdcard/testFiles/errorLog/$now/meminfo
dumpsys activity > /sdcard/testFiles/errorLog/$now/activity