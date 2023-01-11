#!/bin/bash

adb shell "sysctl kernel.sched_pelt_multiplier=$1"
