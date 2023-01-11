#!/bin/bash

adb shell "echo 'menu' > /sys/devices/system/cpu/cpuidle/current_governor"
adb shell "cat /sys/devices/system/cpu/cpuidle/current_governor"
