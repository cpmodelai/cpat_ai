"""Phase 5.4 (D11): a run of one country and two scenarios takes under a second once the data and the baseline run
are cached (core/loop.py), and the cached baseline gives the same results as a fresh one. The bound asserted here is
loose (machines differ); the measured time is printed."""
import time

import pandas as pd

import cpat_model
from cpat_model.core import loop
from cpat_model.inputs import read_scenario_set
from cpat_model.inputs.scenarios import ScenarioSet


def two_scenarios():
    s = read_scenario_set()
    return ScenarioSet(s.rows, s.cols[:2])


def test_cached_run_is_fast_and_identical(capsys):
    loop._BASELINES.clear(), loop._CACHES.clear(), loop._SCENARIOS.clear()
    fresh = cpat_model.run(two_scenarios())
    times = []
    for _ in range(3):
        loop._SCENARIOS.clear()                           # time the policy scenario, with the baseline cached
        t0 = time.perf_counter()
        warm = cpat_model.run(two_scenarios())
        times.append(time.perf_counter() - t0)
    with capsys.disabled():
        print(f'\nrun of Egypt, scenarios 1-2, cached baseline: {min(times):.2f} s (best of 3)')
    assert min(times) < 2.0
    pd.testing.assert_frame_equal(fresh.by_code('EGY'), warm.by_code('EGY'), check_exact=True)
    pd.testing.assert_frame_equal(fresh.distribution_by_code('EGY'), warm.distribution_by_code('EGY'), check_exact=True)
