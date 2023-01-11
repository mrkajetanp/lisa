#!/usr/bin/env python3

import logging
from lisa.utils import setup_logging
from lisa.wa import WAOutput
import pandas as pd
import sys

setup_logging(level=logging.DEBUG)

def trace_cpu_idle_analysis(trace):
    df = trace.df_event("cpu_idle").reset_index()
    df['cluster'] = df['cpu_id'].copy().apply(lambda c: 'little' if c < 4 else 'big' if c > 5 else 'mid')
    #cols = ['Time', 'last_residency_ns', 'time_span_ns', 'sleep_length_ns', 'measured_ns', 'target_residency_ns', 'exit_latency_ns', 'state', 'cluster', '__cpu', '__comm', '__pid']
    #df = df.loc[::, cols]
    return df


path = sys.argv[1]
print("Collecting cpu_idle events for", path)

cpu_idle = WAOutput(path).get_collector(
    'trace',
    trace_to_df=trace_cpu_idle_analysis,
).df

cpu_idle.to_parquet(path + '/cpu_idle.pqt')

print(cpu_idle)
