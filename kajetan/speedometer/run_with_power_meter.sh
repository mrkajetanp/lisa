#!/bin/bash

adb shell "insmod /data/local/sched_tp.ko"
wa run agenda.yaml -d $1
