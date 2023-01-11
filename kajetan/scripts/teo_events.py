#!/usr/bin/env python3

import logging
from lisa.utils import setup_logging
from lisa.wa import WAOutput
import pandas as pd
import sys

setup_logging(level=logging.DEBUG)

def trace_teo_events_analysis(trace):
    df = trace.df_event("trace_printk@func@teo_update").reset_index()
    df['state'] = df['target_residency_ns'].copy().replace(100000, 'C0').replace(83000, 'C0').replace(4488000, 'C1').replace(3934000, 'C1')
    df['cluster'] = df['__cpu'].copy().apply(lambda c: 'little' if c < 4 else 'prime' if c == 7 else 'big')
    cols = ['Time', 'last_residency_ns', 'time_span_ns', 'sleep_length_ns', 'measured_ns', 'target_residency_ns', 'exit_latency_ns', 'state', 'cluster', '__cpu', '__comm', '__pid']
    df = df.loc[::, cols]
    return df


path = sys.argv[1]
print("Collecting TEO events for", path)

teo_events = WAOutput(path).get_collector(
    'trace',
    trace_to_df=trace_teo_events_analysis,
).df

teo_events.to_parquet(path + '/teo_events.pqt')

print(teo_events)
