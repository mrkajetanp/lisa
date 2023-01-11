#!/bin/bash

if [[ -n "$1" ]]; then
	./scripts/clean_cache.py $1
	./scripts/pixel6_emeter.py $1

	./scripts/clean_cache.py $1
	./scripts/cpu_idle.py $1

	./scripts/clean_cache.py $1
	./scripts/cpu_idle_miss.py $1

	./scripts/clean_cache.py $1
	./scripts/latency_wakeup_$2.py $1

	./scripts/clean_cache.py $1
	./scripts/overutilized.py $1

	./scripts/clean_cache.py $1
	./scripts/idle_residency.py $1

	./scripts/clean_cache.py $1
	./scripts/thermal.py $1

	./scripts/clean_cache.py $1
	./scripts/thermal_exynos_power_allocator.py $1

	./scripts/clean_cache.py $1
	./scripts/frequency.py $1

	./scripts/clean_cache.py $1
	./scripts/sched_pelt_cfs.py $1

	./scripts/clean_cache.py $1
	./scripts/tasks_residency.py $1

	./scripts/clean_cache.py $1
	./scripts/latency_wakeup_cgroup.py $1

	./scripts/clean_cache.py $1
	./scripts/task_residency_cgroup.py $1

	./scripts/clean_cache.py $1
	./scripts/energy-estimate.py $1

	./scripts/clean_cache.py $1
else
	echo "Benchmark folder not specified"
fi
