#!/bin/bash

adb shell "sysctl kernel.sched_idleutil_shift=$1"
