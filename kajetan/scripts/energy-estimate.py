#!/usr/bin/env python3

import logging
import pandas as pd
import sys

from lisa.utils import setup_logging
from lisa.wa import WAOutput
from lisa.energy_model import EnergyModel
from lisa.platforms.platinfo import PlatformInfo
from lisa.datautils import series_mean

plat_info = PlatformInfo.from_yaml_map('/home/kajpuc01/power/pixel6/scripts/p6-platform-info.yml')
em = plat_info['nrg-model']

def _energy_estimate(trace):
    return em.estimate_from_trace(trace).reset_index()

def wa_energy_estimate(path):
    return WAOutput(path).get_collector('trace',
                    trace_to_df=_energy_estimate).df

setup_logging(level=logging.DEBUG)

path = sys.argv[1]
print('Collecting energy estimates for', path)

df = wa_energy_estimate(path)
df['little'] = df[['0', '1', '2', '3']].sum(axis=1)
df['mid'] = df[['4', '5']].sum(axis=1)
df['big'] = df[['6', '7']].sum(axis=1)
df['total'] = df[['0', '1', '2', '3', '4', '5', '6', '7']].sum(axis=1)
df['wa_path'] = path

print(df)

df.to_parquet(path + '/energy_estimate.pqt')

# Easier for series_mean and agg.
df.set_index('Time', inplace=True)

df = df.groupby(['workload', 'wa_path', 'kernel', 'iteration']).agg(lambda x: series_mean(x)).reset_index()
df['metric'] = 'energy-estimate'

df.to_parquet(path + '/energy_estimate_mean.pqt')
