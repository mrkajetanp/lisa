#!/usr/bin/env python3

import json
import pandas as pd
import sys, os, glob

path = sys.argv[1]

iterations = sorted(glob.glob(path + '/wk1-*'))

result = pd.DataFrame()

for it in iterations:
    iteration = it[it.rfind('-')+1:]
    df = pd.read_csv(it + '/poller.csv')
    df['iteration'] = int(iteration)
    result = pd.concat([result, df])

with open(path + "/__meta/target_info.json", "r") as f:
    kernel_release = json.loads(f.read())['kernel_release']

result = result.rename(columns={"thermal_zone0-temp":"big",
                                "thermal_zone1-temp":"mid",
                                "thermal_zone2-temp":"little"})

result['wa_path'] = path
result['kernel'] = kernel_release[kernel_release.find('g')+1:-6]
result = result.sort_values(by=['iteration']).reset_index(drop=True)

print(result)
result.to_parquet(path + '/thermal.pqt')
