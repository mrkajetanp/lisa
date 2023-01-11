#!/bin/bash

adb shell "echo 20480 > /dev/cpuctl/background/cpu.shares"
adb shell "echo 20480 > /dev/cpuctl/system-background/cpu.shares"
