#!/usr/bin/env python3

import logging
from lisa.utils import setup_logging
from lisa.wa import WAOutput
import pandas as pd
import sys

setup_logging(level=logging.DEBUG)

def trace_ls_feec_analysis(trace):
    df = trace.df_event("trace_printk@func@find_energy_efficient_cpu").reset_index()
    df['cluster'] = df['__cpu'].copy().apply(lambda c: 'little' if c < 4 else 'big' if c > 5 else 'mid')
    return df


path = sys.argv[1]
print("Collecting feec latency_sensitive traces for", path)

ls_feec = WAOutput(path).get_collector(
    'trace',
    trace_to_df=trace_ls_feec_analysis,
).df

ls_feec.to_parquet(path + '/ls_feec.pqt')

print(ls_feec)
