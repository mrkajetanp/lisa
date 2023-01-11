#!/usr/bin/env python3

import logging
from lisa.utils import setup_logging
from lisa.wa import WAOutput
import pandas as pd
import sys

setup_logging(level=logging.DEBUG)

def trace_thermal_exynos_power_allocator_analysis(trace):
    df = trace.df_event("thermal_exynos_power_allocator").reset_index()
    return df


path = sys.argv[1]
print("Collecting thermal_exynos_power_allocator events for", path)

thermal_exynos_power_allocator = WAOutput(path).get_collector(
    'trace',
    trace_to_df=trace_thermal_exynos_power_allocator_analysis,
).df

thermal_exynos_power_allocator.to_parquet(path + '/thermal_exynos_power_allocator.pqt')

print(thermal_exynos_power_allocator)
