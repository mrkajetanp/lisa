#!/usr/bin/env python3

import sys, os, glob

def clean_cache(path):
    iterations = glob.glob(path + '/wk1-*')
    for it in iterations:
        cache_files = glob.glob(it + '/.*.parquet')
        for f in cache_files:
            try:
                os.remove(f)
            except:
                print('Could not remove ' + str(f))

path = sys.argv[1]
print('Cleaning cache for', path)
clean_cache(path)
