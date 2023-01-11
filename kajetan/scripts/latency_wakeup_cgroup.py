#!/usr/bin/env python3

import logging
from lisa.utils import setup_logging
from lisa.wa import WAOutput
from lisa import wa
from lisa.datautils import series_mean
from lisa.trace import TaskID
import pandas as pd
import sys

setup_logging(level=logging.DEBUG)

def flatten(t):
    return [item for sublist in t for item in sublist]

def wakeup_latency_analysis(trace):
    cpuset_groups = ['/background', '/foreground', '/system-background', '/restricted']
    latencies_list = []
    cgroups = trace.df_event("cgroup_attach_task").reset_index()
    cgroups = cgroups.query("dst_path in @cpuset_groups")

    # breakpoint()

    background_tasks = cgroups.query("dst_path == '/background'") \
        .apply(lambda x: TaskID(x['pid'], x['comm']), axis=1)
    try:
        background_tasks = background_tasks.unique()
    except Exception:
        pass

    foreground_tasks = cgroups.query("dst_path == '/foreground'") \
        .apply(lambda x: TaskID(x['pid'], x['comm']), axis=1)
    try:
        foreground_tasks = foreground_tasks.unique()
    except Exception:
        pass


    system_background_tasks = cgroups.query("dst_path == '/system-background'") \
        .apply(lambda x: TaskID(x['pid'], x['comm']), axis=1)
    try:
        system_background_tasks = system_background_tasks.unique()
    except Exception:
        pass

    for task in background_tasks:
        try:
            latencies = trace.ana.latency.df_latency_wakeup((task.pid, task.comm))
        except Exception:
            continue
        latencies['pid'] = task.pid
        latencies['comm'] = task.comm
        latencies['cgroup'] = 'background'
        latencies_list.append(latencies)

    for task in foreground_tasks:
        try:
            latencies = trace.ana.latency.df_latency_wakeup((task.pid, task.comm))
        except Exception:
            continue
        latencies['pid'] = task.pid
        latencies['comm'] = task.comm
        latencies['cgroup'] = 'foreground'
        latencies_list.append(latencies)

    for task in system_background_tasks:
        try:
            latencies = trace.ana.latency.df_latency_wakeup((task.pid, task.comm))
        except Exception:
            continue
        latencies['pid'] = task.pid
        latencies['comm'] = task.comm
        latencies['cgroup'] = 'system-background'
        latencies_list.append(latencies)

    wakeup_latency = pd.concat(latencies_list)
    return wakeup_latency.reset_index()

path = sys.argv[1]
print("Collecting per-cgroup task wakeup latency for", path)

wakeup_latency = WAOutput(path).get_collector(
    'trace',
    trace_to_df=wakeup_latency_analysis,
).df

print(wakeup_latency)

wakeup_latency.to_parquet(path + '/wakeup_latency_cgroup.pqt')

wakeup_latency_mean = wakeup_latency.groupby(["wa_path", "cgroup", "iteration"]) \
    .agg(lambda x: series_mean(x)).reset_index()[['wa_path', 'iteration', 'cgroup', 'wakeup_latency']] \
    .sort_values(by=['iteration', 'wa_path', 'cgroup'], ascending=[True, True, True])

wakeup_latency_mean.to_parquet(path + '/wakeup_latency_cgroup_mean.pqt')
