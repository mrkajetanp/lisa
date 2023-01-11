#!/usr/bin/env python3

import logging
from lisa.utils import setup_logging
from lisa.wa import WAOutput
from lisa.datautils import series_mean
import pandas as pd
import sys

setup_logging(level=logging.DEBUG)

def trace_frequency_analysis(trace):
    freq = trace.ana.frequency.df_cpus_frequency().reset_index()
    freq['cluster'] = freq['cpu'].copy().apply(lambda c: 'little' if c < 4 else 'big' if c > 5 else 'mid')
    return freq[['Time', 'frequency', 'cluster', 'cpu']]

path = sys.argv[1]
print("Collecting frequency data for", path)

freqs = WAOutput(path).get_collector(
    'trace',
    trace_to_df=trace_frequency_analysis,
).df

freqs.to_parquet(path + '/freqs.pqt')

freqs = freqs.groupby(['wa_path', 'kernel', 'iteration', 'cluster']).agg(lambda x: series_mean(x)).reset_index()
freqs['order'] = freqs['cluster'].replace('little', 0).replace('mid', 1).replace('big', 2)
freqs = freqs.sort_values(by=['iteration', 'order'])[['wa_path', 'kernel', 'iteration', 'cluster', 'frequency']]
freqs['frequency'] = freqs['frequency'] / 1000

freqs.to_parquet(path + '/freqs_mean.pqt')

print(freqs)
