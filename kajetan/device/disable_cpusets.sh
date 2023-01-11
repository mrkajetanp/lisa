#!/bin/bash

adb shell "echo '0-7' > /dev/cpuset/background/cpus"
adb shell "echo '0-7' > /dev/cpuset/foreground/cpus"
adb shell "echo '0-7' > /dev/cpuset/system-background/cpus"
adb shell "echo '0-7' > /dev/cpuset/restricted/cpus"
