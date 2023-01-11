#!/bin/bash

adb shell "echo 'teo' > /sys/devices/system/cpu/cpuidle/current_governor"
adb shell "cat /sys/devices/system/cpu/cpuidle/current_governor"
