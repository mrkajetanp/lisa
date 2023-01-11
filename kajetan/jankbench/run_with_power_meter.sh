#!/bin/bash

#adb shell "insmod /data/local/sched_tp.ko features=__em_sysfs,event__pixel6_emeter,event__sched_util_est_cfs,event__sched_overutilized,event__sched_pelt_cfs,event__sched_cpu_capacity"
adb shell "insmod /data/local/sched_tp.ko"

wa run agenda.yaml -d $1
