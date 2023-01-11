#!/bin/bash

while true; do
	adb shell nohup 'cmd package compile -m speed-profile -f -a'
done

