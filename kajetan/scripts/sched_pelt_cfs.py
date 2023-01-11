#!/usr/bin/env python3

import logging
from lisa.utils import setup_logging
from lisa.wa import WAOutput
from lisa.datautils import series_mean
import pandas as pd
import sys

setup_logging(level=logging.DEBUG)

def sched_pelt_cfs_analysis(trace):
    df = trace.df_event("sched_pelt_cfs").reset_index()
    df['cluster'] = df['cpu'].copy().apply(lambda c: 'little' if c < 4 else 'big' if c > 5 else 'mid')
    return df

path = sys.argv[1]
print("Collecting sched_pelt_cfs for", path)

sched_pelt_cfs = WAOutput(path).get_collector(
    'trace',
    trace_to_df=sched_pelt_cfs_analysis,
).df

sched_pelt_cfs.to_parquet(path + '/sched_pelt_cfs.pqt')

print(sched_pelt_cfs)

sched_pelt_cfs = sched_pelt_cfs.query("path == '/'") \
    [['cluster', 'load', 'util', 'iteration', 'wa_path', 'kernel']] \
    .groupby(['wa_path', 'iteration', 'cluster']).agg(lambda x: series_mean(x)).reset_index() \
    .sort_values(by=['wa_path', 'iteration'])

sched_pelt_cfs.to_parquet(path + '/sched_pelt_cfs_mean.pqt')

print(sched_pelt_cfs)
