#!/usr/bin/env python3

import logging
from lisa.utils import setup_logging
from lisa.wa import WAOutput
from lisa import wa
from lisa.trace import TaskID
import pandas as pd
import sys

setup_logging(level=logging.DEBUG)

def trim_task(task):
    idx = task.find(':')
    return task[idx+1:-1]

def task_residency_analysis(trace):
    cpuset_groups = ['/background', '/foreground', '/system-background', '/restricted']
    cgroups = trace.df_event("cgroup_attach_task").reset_index()
    cgroups = cgroups.query("dst_path in @cpuset_groups")

    background_tasks = cgroups.query("dst_path == '/background'") \
        .apply(lambda x: (x['pid'], x['comm']), axis=1)
    try:
        background_tasks = background_tasks.unique()
    except Exception:
        pass

    foreground_tasks = cgroups.query("dst_path == '/foreground'") \
        .apply(lambda x: (x['pid'], x['comm']), axis=1)
    try:
        foreground_tasks = foreground_tasks.unique()
    except Exception:
        pass

    system_background_tasks = cgroups.query("dst_path == '/system-background'") \
        .apply(lambda x: (x['pid'], x['comm']), axis=1)
    try:
        system_background_tasks = system_background_tasks.unique()
    except Exception:
        pass

    background_tasks_residency = trace.ana.tasks.df_tasks_total_residency(list(background_tasks))
    background_tasks_residency['cgroup'] = 'background'

    foreground_tasks_residency = trace.ana.tasks.df_tasks_total_residency(list(foreground_tasks))
    foreground_tasks_residency['cgroup'] = 'foreground'

    system_background_tasks_residency = trace.ana.tasks.df_tasks_total_residency(list(system_background_tasks))
    system_background_tasks_residency['cgroup'] = 'system-background'

    task_residency = pd.concat([background_tasks_residency, foreground_tasks_residency, system_background_tasks_residency]).reset_index()

    task_residency['comm'] = task_residency['index'].map(trim_task).astype(str)
    task_residency['little'] = task_residency[[0.0, 1.0, 2.0, 3.0]].sum(axis=1)
    task_residency['mid'] = task_residency[[4.0, 5.0]].sum(axis=1)
    task_residency['big'] = task_residency[[6.0, 7.0]].sum(axis=1)
    task_residency = task_residency.rename(columns={col:str(col) for col in task_residency.columns})
    task_residency = task_residency.groupby(["comm", "cgroup"]).sum().sort_values(by='Total', ascending=False).reset_index()

    return task_residency.reset_index()

path = sys.argv[1]
print("Collecting per-cgroup task residency for", path)

task_residency = WAOutput(path).get_collector(
    'trace',
    trace_to_df=task_residency_analysis,
).df

print(task_residency)

task_residency.to_parquet(path + '/task_residency_cgroup.pqt')

task_residency_total = task_residency.groupby(["wa_path", "cgroup", "iteration"]) \
    .sum().reset_index() \
    .sort_values(by=['iteration', 'wa_path', 'cgroup', 'Total'], ascending=[True, True, True, False])

task_residency_total.to_parquet(path + '/task_residency_cgroup_total.pqt')
