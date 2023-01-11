#!/usr/bin/env python3

import logging
from lisa.utils import setup_logging
from lisa.wa import WAOutput
from lisa.datautils import series_mean
import pandas as pd
import sys

setup_logging(level=logging.DEBUG)

def trace_pixel6_emeter_analysis(trace):
    df = trace.df_event("pixel6_emeter").reset_index()

    p6_emeter_labels = {
        'S4M_VDD_CPUCL0': 'little',
        'S3M_VDD_CPUCL1': 'mid',
        'S2M_VDD_CPUCL2': 'big',
    }

    df = df.pivot_table(values='value', index='ts', columns='chan_name').reset_index().rename(columns=p6_emeter_labels)[['ts', 'little', 'mid', 'big']]
    df["little_energy"] = df["little"].diff()
    df["mid_energy"] = df["mid"].diff()
    df["big_energy"] = df["big"].diff()
    df['ts_diff'] = df['ts'].diff()

    df["little_power"] = df["little_energy"] / df["ts_diff"]
    df["mid_power"] = df["mid_energy"] / df["ts_diff"]
    df["big_power"] = df["big_energy"] / df["ts_diff"]

    return df


path = sys.argv[1]
print("Collecting pixel6_emeter events for", path)

pixel6_emeter = WAOutput(path).get_collector(
    'trace',
    trace_to_df=trace_pixel6_emeter_analysis,
).df

pixel6_emeter.to_parquet(path + '/pixel6_emeter.pqt')

pixel6_emeter = pixel6_emeter.groupby(['wa_path', 'kernel', 'iteration']).agg(lambda x: series_mean(x)).reset_index()

pixel6_emeter.to_parquet(path + '/pixel6_emeter_mean.pqt')

print(pixel6_emeter)
