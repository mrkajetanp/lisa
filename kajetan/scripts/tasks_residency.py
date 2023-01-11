#!/usr/bin/env python3

import logging
from lisa.utils import setup_logging
from lisa.wa import WAOutput
from lisa.datautils import series_mean
import pandas as pd
import sys

setup_logging(level=logging.DEBUG)

def trim_task(task):
    idx = task.find(':')
    return task[idx+1:-1]

def trace_tasks_residency_time_analysis(trace):
    df = trace.ana.tasks.df_tasks_total_residency().reset_index()
    df['comm'] = df['index'].map(trim_task).astype(str)
    df['little'] = df[[0.0, 1.0, 2.0, 3.0]].sum(axis=1)
    df['mid'] = df[[4.0, 5.0]].sum(axis=1)
    df['big'] = df[[6.0, 7.0]].sum(axis=1)
    df = df.rename(columns={col:str(col) for col in df.columns})
    df = df.groupby("comm").sum().sort_values(by='Total', ascending=False).reset_index()
    return df

path = sys.argv[1]
print("Computing residencies for", path)

tasks_residency_time = WAOutput(path).get_collector(
    'trace',
    trace_to_df=trace_tasks_residency_time_analysis,
).df

tasks_residency_time.to_parquet(path + '/tasks_residency.pqt')

tasks_residency_time = tasks_residency_time.query("not comm.str.startswith('swapper')")
tasks_residency_time = tasks_residency_time.groupby(['wa_path', 'kernel', 'iteration']).sum().reset_index()

tasks_residency_time.to_parquet(path + '/tasks_residency_total.pqt')

print(tasks_residency_time)
