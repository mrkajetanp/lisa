#!/usr/bin/python3

import os

def set_schedattr_prefer_idle(comm="surfaceflinger"):
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
        os.system("adb shell '/data/local/uclamp_tool -p %d -i'" % (task_pid))

set_schedattr_prefer_idle(comm="surfaceflinger")
set_schedattr_prefer_idle(comm="RenderThread")
set_schedattr_prefer_idle(comm="chmark:workload")
set_schedattr_prefer_idle(comm="CrRendererMain")
set_schedattr_prefer_idle(comm="droid.benchmark")
