#!/bin/bash

adb shell "echo 1 > /dev/cpuctl/system/cpu.uclamp.boosted"
LATENCY_SENSITIVE=$(adb shell "cat /dev/cpuctl/system/cpu.uclamp.boosted")
adb shell "echo latency_sensitive: $LATENCY_SENSITIVE"
