#!/usr/bin/python3

import os

def set_schedattr_uclamp_min(uclamp_min=0, comm="surfaceflinger"):
    output = os.popen("adb shell 'ps -A | grep %s'" % comm).read()
    print(output)
    spl = output.split('\n')
    print(spl)
    for line in spl:
        if line == '':
            break
        ou = line.strip().split()
        task_pid = int(ou[1])
        print("found pid=%d" % task_pid)
        os.system("adb shell '/data/local/uclamp_tool -m %d -p %d'" % (uclamp_min, task_pid))

set_schedattr_uclamp_min(uclamp_min=20, comm="surfaceflinger")
#set_schedattr_uclamp_min(uclamp_min=20, comm="RenderThread")
#set_schedattr_uclamp_min(uclamp_min=20, comm="com.android.benchmark")
