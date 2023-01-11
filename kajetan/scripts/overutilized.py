#!/usr/bin/env python3

import logging
from lisa.utils import setup_logging
from lisa.wa import WAOutput
import pandas as pd
import sys

setup_logging(level=logging.DEBUG)

def trace_overutilized_analysis(trace):
    df = pd.DataFrame()
    time = trace.ana.status.get_overutilized_time()
    total_time = trace.time_range
    perc = round(time / total_time * 100, 2)
    return df.append({'time':time, 'total_time':total_time, 'percentage':perc}, ignore_index=True)


path = sys.argv[1]
print("Collecting overutilized events for", path)

overutilized = WAOutput(path).get_collector(
    'trace',
    trace_to_df=trace_overutilized_analysis,
).df

overutilized.to_parquet(path + '/overutilized.pqt')

print(overutilized)
