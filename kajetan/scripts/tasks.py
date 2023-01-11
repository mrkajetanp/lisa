#!/usr/bin/env python3

import logging
from lisa.utils import setup_logging
from lisa.wa import WAOutput
import pandas as pd
import sys

setup_logging(level=logging.DEBUG)

def trace_tasks_analysis(trace):
    tasks = trace.ana.tasks.df_tasks_total_residency()
    tasks = tasks.rename(columns={0.0:'cpu0', 1.0:'cpu1', 2.0:'cpu2', 3.0:'cpu3', 4.0:'cpu4', 5.0:'cpu5', 6.0:'cpu6', 7.0:'cpu7'}).reset_index()
    return tasks

path = sys.argv[1]
print("Collecting tasks data for", path)

tasks = WAOutput(path).get_collector(
    'trace',
    trace_to_df=trace_tasks_analysis,
).df

tasks.to_parquet(path + '/tasks.pqt')

print(tasks)
