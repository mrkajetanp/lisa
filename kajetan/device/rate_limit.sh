#!/bin/bash

adb shell "echo '0' > /sys/devices/system/cpu/cpu0/cpufreq/schedutil/rate_limit_us"
adb shell "echo '0' > /sys/devices/system/cpu/cpu1/cpufreq/schedutil/rate_limit_us"
adb shell "echo '0' > /sys/devices/system/cpu/cpu2/cpufreq/schedutil/rate_limit_us"
adb shell "echo '0' > /sys/devices/system/cpu/cpu3/cpufreq/schedutil/rate_limit_us"
adb shell "echo '0' > /sys/devices/system/cpu/cpu4/cpufreq/schedutil/rate_limit_us"
adb shell "echo '0' > /sys/devices/system/cpu/cpu5/cpufreq/schedutil/rate_limit_us"
adb shell "echo '0' > /sys/devices/system/cpu/cpu6/cpufreq/schedutil/rate_limit_us"
adb shell "echo '0' > /sys/devices/system/cpu/cpu7/cpufreq/schedutil/rate_limit_us"

adb shell "cat /sys/devices/system/cpu/cpu0/cpufreq/schedutil/rate_limit_us"
adb shell "cat /sys/devices/system/cpu/cpu4/cpufreq/schedutil/rate_limit_us"
adb shell "cat /sys/devices/system/cpu/cpu7/cpufreq/schedutil/rate_limit_us"
