#!/usr/bin/python

import os
import sys

comm = sys.argv[1]

output = os.popen("adb shell 'ps -e | grep %s'" % comm).read()
lines = output.split('\n')[:-1]
for line in lines:
    parts = line.split()
    pid = parts[1]
    print(os.system("adb shell 'cat /proc/{}/sched'".format(pid)))
    print(os.system("adb shell 'cat /proc/{}/cgroup'".format(pid)))
