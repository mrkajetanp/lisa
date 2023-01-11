#!/usr/bin/env python3

import logging
from lisa.utils import setup_logging
from lisa.wa import WAOutput
import pandas as pd
import sys

setup_logging(level=logging.DEBUG)

def trace_cgroup_attach_task_analysis(trace):
    df = trace.df_event("cgroup_attach_task").reset_index()
    return df


path = sys.argv[1]
print("Collecting cgroup_attach_task events for", path)

cgroup_attach_task = WAOutput(path).get_collector(
    'trace',
    trace_to_df=trace_cgroup_attach_task_analysis,
).df

cgroup_attach_task.to_parquet(path + '/cgroup_attach_task.pqt')

print(cgroup_attach_task)
