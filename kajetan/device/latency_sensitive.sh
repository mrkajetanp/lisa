#!/bin/bash

adb shell "echo 1 > /dev/cpuctl/system/cpu.uclamp.latency_sensitive"
LATENCY_SENSITIVE=$(adb shell "cat /dev/cpuctl/system/cpu.uclamp.latency_sensitive")
adb shell "echo latency_sensitive: $LATENCY_SENSITIVE"
