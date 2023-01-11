#!/bin/bash

adb root

LTL_CPUFREQ=$(adb shell "cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor")
MID_CPUFREQ=$(adb shell "cat /sys/devices/system/cpu/cpu4/cpufreq/scaling_governor")
BIG_CPUFREQ=$(adb shell "cat /sys/devices/system/cpu/cpu7/cpufreq/scaling_governor")

adb shell "echo BIG cpufreq $BIG_CPUFREQ"
adb shell "echo MID cpufreq $MID_CPUFREQ"
adb shell "echo LTL cpufreq $LTL_CPUFREQ"

BIG_TEMP=$(adb shell "cat /sys/class/thermal/thermal_zone0/temp")
MID_TEMP=$(adb shell "cat /sys/class/thermal/thermal_zone1/temp")
LTL_TEMP=$(adb shell "cat /sys/class/thermal/thermal_zone2/temp")

adb shell "echo BIG $BIG_TEMP"
adb shell "echo MID $MID_TEMP"
adb shell "echo LTL $LTL_TEMP"

LATENCY_SENSITIVE=$(adb shell "cat /dev/cpuctl/system/cpu.uclamp.latency_sensitive")
IDLE_GOVERNOR=$(adb shell "cat /sys/devices/system/cpu/cpuidle/current_governor_ro")
adb shell "echo latency_sensitive: $LATENCY_SENSITIVE"
adb shell "echo idle governor: $IDLE_GOVERNOR"

CPUSET_BG=$(adb shell "cat /dev/cpuset/background/cpus")
CPUSET_FG=$(adb shell "cat /dev/cpuset/foreground/cpus")
CPUSET_SBG=$(adb shell "cat /dev/cpuset/system-background/cpus")
CPUSET_RES=$(adb shell "cat /dev/cpuset/restricted/cpus")

echo cpusets: background: $CPUSET_BG, foreground: $CPUSET_FG, system-bg: $CPUSET_SBG, res: $CPUSET_RES

CPUSHARES_BG=$(adb shell "cat /dev/cpuctl/background/cpu.shares")
CPUSHARES_FG=$(adb shell "cat /dev/cpuctl/foreground/cpu.shares")
CPUSHARES_SBG=$(adb shell "cat /dev/cpuctl/system-background/cpu.shares")
CPUSHARES_SYS=$(adb shell "cat /dev/cpuctl/system/cpu.shares")

echo cpu.shares: background: $CPUSHARES_BG, foreground: $CPUSHARES_FG, system-bg: $CPUSHARES_SBG, system: $CPUSHARES_SYS


adb shell "sysctl kernel.sched_pelt_multiplier"
