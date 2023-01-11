# Introduction

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED

Jokes aside, this is just how I set up my testing environment to make it easier for myself. It might break in funny ways here and there.

# Structure

The following is what the directory structure necessary for my testing framework to work is:

```
├── device                                 <-- contains scripts for controlling the device through adb
│   ├── status.sh                          <-- sets adb to root and prints out the relevant system information
│   ├── teo.sh                             <-- sets the cpuidle governor to TEO
├── geekbench                              <-- contains the GB5 test runs and scripts
│   ├── agenda.yaml                        <-- agenda used by workload-automation
│   ├── geekbench_baseline_3_0812          <-- example benchmark run directory produced by WA
│   ├── geekbench_baseline_ufc_3_1001
│   └── run_with_power_meter.sh            <-- script to inject the lisa module assuming it's in /data/local/sched_tp.ko and run the test
├── jankbench
│   ├── agenda.yaml
│   ├── jankbench_baseline_60hz_10_0812
│   └── run_with_power_meter.sh
├── scripts                                <-- contains scripts for extracting data from traces into .pqt files in benchmark run directories
│   ├── latency_wakeup_geekbench.py        <-- extracts wakeup latencies of tasks relevant for GB5
│   ├── latency_wakeup_jank.py             <-- as above but for jankbench
│   ├── process_workload.sh                <-- runs the full suite of scripts in sequence. might take multiple hours.
└── speedometer
    ├── agenda.yaml
    ├── speedometer_baseline_10_0812
    └── run_with_power_meter.sh
```

# Running the test

To run a test, first flash the relevant kernel onto the device and set up the environment. Example:

```
(flash the kernel here)
device/status.sh          <-- set adb to root and check the system state
device/teo.sh             <-- change the idle governor to TEO
cd geekbench/
./run_with_power_meter.sh geekbench_teo_3_1101
```

## Naming scheme

All my scripts and notebooks rely on the naming scheme being:

`<benchmark_name>_<arbitary_tag>_<iterations>_<date_in_DDMM_format>`

If it's not followed, all the notebooks will break immediately so I wouldn't recommend.
I automatically trim the names to only keep the tag on actual plots and in tables but that obviously relies on character counts.

# Extracting results

The benchmark scores and perf numbers will be there automatically so once the test is done, nothing left to do.
Extracting data from traces, however, requires calling into scripts that use LISA.

To continue the above example:

`scripts/process_workload.sh geekbench/geekbench_teo_3_1101 geekbench`

The 'geekbench' at the end is the suffix used by the script to distinguish which latency extracting script to use.
It corresponds to the latency suffixes on scripts like latency_wakeup_geekbench.py etc.

If you're only interested in some of the data you can call the scripts directly:
E.g. this one will extract the power usage numbers.

`scripts/pixel6_emeter.py geekbench/geekbench_teo_3_1101`

Just make sure to also clean the cache in between different scripts because if the LISA cache is still present it'll break the results.

`scripts/clean_cache.py geekbench/geekbench_teo_3_1101`

Those scripts can take ages to finish, especially when many iterations are present.
10 iterations of Jankbench on my 10th gen i7 ThinkPad can take over 15 hours for the entire process_workload.sh..

# Reading the results

Luckily, once processed the resulting .pqts can be read into Pandas on the command line or into a notebook instantly.

My notebooks can be found under ipynb/linux-pm

The variable BENCHMARK_PATH under Setup needs to be set to the directory with runs of the respective benchmarks.
Then, benchmark_name_[a-e] can be set to 5 arbitrary runs of the benchmark that will then be plotted and compared against each other.
benchmark_name_a is used as the baseline so that's what the percentages are in relation to.
For bar plots, the columns including asterisks mean that the pvalues were sufficiently low.

I needed 5 way-comparisons for the most recent tests I was doing (hence the 5w_*) namings but it can easily be reduced down by tweaking the python code.

Overall the idea is the same for the entire notebook. Each metric, e.g. power usage, will read in the .pqts produced by the scripts mentioned above.
Then they'll be combined into one big dataframe and processed in whichever way is needed to display them.

This of course relies on there being .pqts for all 5 runs but again that can be adjusted in the code and reduced in a few minutes as needed.

## Notebooks

The different `5w_<benchmark>_full.ipynb` notebooks are meant to be roughly the same with benchmark-related differences.
I update them as needed so there might be small discrepancies here and there.
