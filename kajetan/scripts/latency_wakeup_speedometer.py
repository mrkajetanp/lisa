#!/usr/bin/env python3

import logging
from lisa.utils import setup_logging
from lisa.wa import WAOutput
from lisa.datautils import series_mean
import pandas as pd
import sys

setup_logging(level=logging.DEBUG)

def flatten(t):
    return [item for sublist in t for item in sublist]

def wakeup_latency_analysis(trace):
    tasks = [
        trace.get_task_ids('CrRendererMain'),
        trace.get_task_ids('ThreadPoolForeg'),
        trace.get_task_ids('.android.chrome'),
        trace.get_task_ids('CrGpuMain'),
        trace.get_task_ids('Compositor'),
        trace.get_task_ids('Chrome_IOThread'),
        trace.get_task_ids('surfaceflinger'),
        trace.get_task_ids('RenderThread'),
    ]

    latency_list = []
    for pid, comm in flatten(tasks):
        latencies = trace.ana.latency.df_latency_wakeup((pid, comm))
        latencies['pid'] = pid
        latencies['comm'] = comm
        latency_list.append(latencies)

    wakeup_latency = pd.concat(latency_list)
    return wakeup_latency.reset_index()

path = sys.argv[1]
print("Collecting task wakeup latency for", path)

wakeup_latency = WAOutput(path).get_collector(
    'trace',
    trace_to_df=wakeup_latency_analysis,
).df

print(wakeup_latency)

wakeup_latency.to_parquet(path + '/wakeup_latency.pqt')

wakeup_latency_mean = wakeup_latency.groupby(['wa_path', 'kernel', 'iteration', 'comm']) \
    .agg(lambda x: series_mean(x)).reset_index()[['wa_path', 'kernel', 'iteration', 'comm', 'wakeup_latency']].sort_values(by=['iteration', 'comm'], ascending=[True, True])

wakeup_latency_mean.to_parquet(path + '/wakeup_latency_mean.pqt')
