#!/usr/bin/env python3

import pandas as pd
import sys, os, glob

path = sys.argv[1]

files = glob.glob(path + '/*.pqt')
for file in files:
    print('updating', file)
    df = pd.read_parquet(file)
    df['wa_path'] = path
    print(df)
    df.to_parquet(file)
