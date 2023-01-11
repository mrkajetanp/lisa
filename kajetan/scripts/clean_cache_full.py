#!/usr/bin/env python3

import sys, os, glob, shutil

def clean_cache(path):
    iterations = glob.glob(path + '/wk1-pcmark-*')
    for it in iterations:
        cache_files = glob.glob(it + '/.*.parquet')
        for f in cache_files:
            try:
                os.remove(f)
            except:
                print('Could not remove ' + str(f))

        cache_files = glob.glob(it + '/.*.lisa-swap')
        for f in cache_files:
            try:
                shutil.rmtree(f)
            except:
                print('Could not remove ' + str(f))



path = sys.argv[1]
print('Cleaning full cache for', path)
clean_cache(path)
