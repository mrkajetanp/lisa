#!/usr/bin/env python3

import logging
from lisa.utils import setup_logging
from lisa.wa import WAOutput
import pandas as pd
import sys

setup_logging(level=logging.DEBUG)

def trace_cpu_idle_miss_analysis(trace):
    df = trace.df_event("cpu_idle_miss").reset_index()
    df['cluster'] = df['cpu_id'].copy().apply(lambda c: 'little' if c < 4 else 'big' if c > 5 else 'mid')
    return df


path = sys.argv[1]
print("Collecting cpu_idle_miss events for", path)

cpu_idle_miss = WAOutput(path).get_collector(
    'trace',
    trace_to_df=trace_cpu_idle_miss_analysis,
).df

cpu_idle_miss.to_parquet(path + '/cpu_idle_miss.pqt')

cpu_idle_miss = cpu_idle_miss.groupby(['wa_path', 'cluster', 'below'], as_index=False).size()
cpu_idle_miss['order'] = cpu_idle_miss['cluster'].replace('little', 0).replace('mid', 1).replace('big', 2)
cpu_idle_miss = cpu_idle_miss.sort_values(by=['order'])[['wa_path', 'cluster', 'below', 'size']].rename(columns={'size':'count'})

cpu_idle_miss.to_parquet(path + '/cpu_idle_miss_counts.pqt')

print(cpu_idle_miss)
