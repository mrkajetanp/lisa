#!/usr/bin/env python3

import logging
from lisa.utils import setup_logging
from lisa.wa import WAOutput
from lisa.datautils import series_mean
import pandas as pd
import sys

setup_logging(level=logging.DEBUG)

def trace_power_meter_analysis(trace):
    df = trace.df_event("power_meter").reset_index()

    power_meter_labels = {
        'ch3': 'big',
        'ch4': 'mid',
        'ch5': 'little',
    }

    df = df.rename(columns=power_meter_labels)

    df["little_energy"] = df["little"].diff()
    df["mid_energy"] = df["mid"].diff()
    df["big_energy"] = df["big"].diff()
    df["ts_diff"] = df["timestamp"].diff()

    df["little_power"] = df["little_energy"] / df["ts_diff"]
    df["mid_power"] = df["mid_energy"] / df["ts_diff"]
    df["big_power"] = df["big_energy"] / df["ts_diff"]

    return df


path = sys.argv[1]
print("Collecting power_meter events for", path)

power_meter = WAOutput(path).get_collector(
    'trace',
    trace_to_df=trace_power_meter_analysis,
).df

power_meter.to_parquet(path + '/power_meter.pqt')

power_meter = power_meter.groupby(['wa_path', 'kernel', 'iteration']).agg(lambda x: series_mean(x)).reset_index()

power_meter.to_parquet(path + '/power_meter_mean.pqt')

print(power_meter)
