#!/bin/bash

adb shell "echo 'shallow' > /sys/devices/system/cpu/cpuidle/current_governor"
adb shell "cat /sys/devices/system/cpu/cpuidle/current_governor"
