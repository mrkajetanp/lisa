#!/usr/bin/env python3

import logging
from lisa.utils import setup_logging
from lisa.wa import WAOutput
import pandas as pd
import sys

setup_logging(level=logging.DEBUG)

def trace_idle_residency_time_analysis(trace):
    cluster_little = [0, 1, 2, 3]
    cluster_mid = [4, 5]
    cluster_big = [6, 7]

    df_little = trace.ana.idle.df_cluster_idle_state_residency(cluster_little).reset_index().sort_values(by=['idle_state'])
    df_little['cluster'] = 'little'
    df_mid = trace.ana.idle.df_cluster_idle_state_residency(cluster_mid).reset_index().sort_values(by=['idle_state'])
    df_mid['cluster'] = 'mid'
    df_big = trace.ana.idle.df_cluster_idle_state_residency(cluster_big).reset_index().sort_values(by=['idle_state'])
    df_big['cluster'] = 'big'

    return pd.concat([df_little, df_mid, df_big])

path = sys.argv[1]
print("Computing residencies for", path)

idle_residency_time = WAOutput(path).get_collector(
    'trace',
    trace_to_df=trace_idle_residency_time_analysis,
).df

idle_residency_time.to_parquet(path + '/idle_residency.pqt')

print(idle_residency_time)
